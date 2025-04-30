import binascii
import csv
import hashlib
import logging
import sys
import os
import ssl
import requests
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple, Union
from urllib.parse import urljoin
from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from ._internal import Intermediates as RustIntermediates, PyCRLiteClubcard, PyCRLiteStatus
from crlite_python.exceptions import *


OID_SCT_EXTENSION = "1.3.6.1.4.1.11129.2.4.2"

ICA_LIST_URL = "https://ccadb.my.salesforce-sites.com/mozilla/MozillaIntermediateCertsCSVReport"

STAGE_ATTACH_URL = "https://firefox-settings-attachments.cdn.allizom.org/"
STAGE_URL = "https://firefox.settings.services.allizom.org/v1/buckets/security-state-staging/collections/"

PROD_ATTACH_URL = "https://firefox-settings-attachments.cdn.mozilla.net/"
PROD_URL = "https://firefox.settings.services.mozilla.com/v1/buckets/security-state-staging/collections/"



class Status(Enum):
	EXPIRED = "Expired"
	GOOD = "Good"
	NOT_COVERED = "NotCovered"
	NOT_ENROLLED = "NotEnrolled"
	REVOKED = "Revoked"

class CRLiteFilterChannel(Enum):
	"""Defines the CRlite revocation information channel.
	Only Default and Compat are enabled currently.
	"""
	ExpermentalDeltas = "experimental+deltas"
	Default = "default"
	Compat = "compat"


@dataclass
class CertRevCollection:
	data: List['CertRevRecord']

	@staticmethod
	def from_json(json_data: dict) -> 'CertRevCollection':
		return CertRevCollection([CertRevRecord.from_json(item) for item in json_data.get('data', [])])

@dataclass
class CertRevRecord:
	attachment: 'CertRevRecordAttachment'
	incremental: bool
	channel: Optional['CRLiteFilterChannel']

	@staticmethod
	def from_json(json_data: dict) -> 'CertRevRecord':
		attachment_data = json_data.get('attachment', {})
		attachment = CertRevRecordAttachment.from_json(attachment_data)
		incremental = json_data.get('incremental', False)
		channel_str = json_data.get('channel')
		channel = CRLiteFilterChannel(channel_str) if channel_str else None
		return CertRevRecord(attachment, incremental, channel)

@dataclass
class CertRevRecordAttachment:
	hash: str
	filename: str
	location: str

	@staticmethod
	def from_json(json_data: dict) -> 'CertRevRecordAttachment':
		hash = json_data.get('hash', '')
		filename = json_data.get('filename', '')
		location = json_data.get('location', '')
		return CertRevRecordAttachment(hash, filename, location)


def _update_intermediates(db_dir: Path) -> None:
	intermediates_path = db_dir / "crlite.intermediates"
	logging.info(f"Fetching {ICA_LIST_URL}")
	try:
		response = requests.get(ICA_LIST_URL)
		response.raise_for_status()
		intermediates_bytes = response.content
	except requests.exceptions.RequestException as e:
		raise CRLiteDBError(f"Could not fetch CCADB report: {e}")

	try:
		intermediates = Intermediates.from_ccadb_csv(intermediates_bytes)
	except Exception as e:
		raise CRLiteDBError(f"Cannot parse CCADB report: {e}")

	try:
		encoded_intermediates = intermediates.to_bincode()
		with open(intermediates_path, "wb") as f:
			f.write(encoded_intermediates)
	except Exception as e:
		raise CRLiteDBError(f"Error writing intermediates file: {e}")


class Intermediates:
	# def __init__(self, intermediates: Dict[bytes, List[bytes]]):
	# 	self.intermediates = intermediates
	def __new__(self):
		return RustIntermediates()

	@staticmethod
	def from_ccadb_csv(bytes_data: bytes) -> 'RustIntermediates':
		inter_obj = Intermediates()
		text = bytes_data.decode('utf-8', errors='ignore')
		reader = csv.reader(text)
		for row in reader:
			if row and row[0] and row[0].startswith('-----BEGIN CERTIFICATE-----'):
				try:
					pem_data = row[0].encode('utf-8')
					cert_obj = x509.load_pem_x509_certificate(pem_data)
					issuer_dn = cert_obj.subject.public_bytes(serialization.Encoding.DER)
					der_cert = cert_obj.public_bytes(serialization.Encoding.DER)
					if issuer_dn not in inter_obj.intermediates:
						inter_obj.add_cert(issuer_dn, der_cert)
				except Exception as e:
					logging.warning(f"Error processing CCADB record: {e}")
		return inter_obj

	@staticmethod
	def decode(bytes_data: bytes) -> 'RustIntermediates':
		return RustIntermediates.from_bincode(bytes_data)



	def lookup_issuer_spki(self, cert: x509.Certificate) -> Optional[bytes]:
		try:
			# cert = x509.load_der_x509_certificate(cert_bytes)
			issuer_dn = cert.issuer.public_bytes(serialization.Encoding.DER)
			if issuer_dn in self.intermediates:
				for der_issuer_cert in self.intermediates[issuer_dn]:
					try:
						issuer = x509.load_der_x509_certificate(der_issuer_cert)
						issuer_spki = issuer.public_key()

						# If the cert was signed by the issuer, this function returns None.
						# Else, it can raise either ValueError, TypeError, or InvalidSignature
						cert.verify_directly_issued_by(issuer)
						return issuer_spki.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)

					except (TypeError, InvalidSignature) as e:
						logging.debug(f"Issue validating signature: {e}")
						pass

					except Exception as e:
						logging.warning(f"Error parsing intermediate certificate: {e}")
		except Exception as e:
			logging.warning(f"Error parsing target certificate: {e}")
		return None

class Filter:
	def __init__(self, filter_obj: Optional['PyCRLiteClubcard']):
		self.filter = filter_obj
		# test = rs_crlite.PyCR

	@staticmethod
	def from_bytes(bytes_data: bytes) -> 'Filter':
		try:
			clubcard = PyCRLiteClubcard.load_filter(bytes_data)
			return Filter(clubcard)
		except Exception as e:
			raise CRLiteDBError(f"Could not load filter: {e}")

	def has(self, issuer_spki_hash: bytes, serial: bytes, timestamps: List[Tuple[bytes, int]]) -> 'PyCRLiteStatus':
		status = PyCRLiteStatus.NotCovered
		if self.filter:
			status = self.filter.query_filter(self.filter, issuer_spki_hash, serial, timestamps)
		return status


def _update_db(db_dir: Path, attachment_url: str, base_url: str, channel: 'CRLiteFilterChannel') -> None:
	logging.info(f"Fetching cert-revocations records from remote settings {base_url}")
	try:
		response = requests.get(urljoin(base_url, "cert-revocations/records"))
		response.raise_for_status()
		cert_rev_records = CertRevCollection.from_json(response.json())
	except requests.exceptions.RequestException as e:
		raise CRLiteDBError(f"Could not fetch remote settings collection: {e}")
	except Exception as e:
		raise CRLiteDBError(f"Could not read remote settings data: {e}")

	filters = [f for f in cert_rev_records.data if f.channel == channel]
	full_filters_count = sum(1 for f in filters if not f.incremental)

	if full_filters_count != 1:
		raise CRLiteDBError("Number of full filters found in remote settings is not 1")

	expected_filenames = {f.attachment.filename for f in filters}

	for entry in os.listdir(db_dir):
		entry_path = db_dir / entry
		if entry_path.is_file():
			extension = entry_path.suffix[1:]
			if (extension == "delta" or extension == "filter") and entry not in expected_filenames:
				logging.info(f"Removing {entry}")
				try:
					os.remove(entry_path)
				except OSError as e:
					logging.warning(f"Could not remove {entry}: {e}")

	for filter_record in filters:
		expected_digest = binascii.unhexlify(filter_record.attachment.hash)
		path = db_dir / filter_record.attachment.filename
		if path.exists():
			try:
				with open(path, "rb") as f:
					content = f.read()
				digest = hashlib.sha256(content).digest()
				if expected_digest == digest:
					logging.info(f"Found existing copy of {filter_record.attachment.filename}")
					continue
			except OSError as e:
				logging.warning(f"Error reading existing filter {path}: {e}")

		filter_url = urljoin(attachment_url, filter_record.attachment.location)
		logging.info(f"Fetching {filter_record.attachment.filename} from {filter_url}")
		try:
			response = requests.get(filter_url)
			response.raise_for_status()
			filter_bytes = response.content
		except requests.exceptions.RequestException as e:
			raise CRLiteDBError(f"Could not fetch filter: {e}")

		digest = hashlib.sha256(filter_bytes).digest()
		if expected_digest != digest:
			raise CRLiteDBError("Filter digest mismatch")

		try:
			with open(path, "wb") as f:
				f.write(filter_bytes)
		except OSError as e:
			raise CRLiteDBError(f"Could not write filter to {path}: {e}")


class CRLiteDB:
	"""CRLite Database contains the Clubcard filters and Intermediates certificate info
	"""
	def __init__(self, db_dir: Path, filters: List[Filter], intermediates: Intermediates):
		self.db_dir = db_dir
		self.filters = filters
		self.intermediates = intermediates

	@staticmethod
	def load(db_dir: Path) -> 'CRLiteDB':

		filters = []
		for entry in os.listdir(db_dir):
			entry_path = db_dir / entry
			if entry_path.is_file():
				extension = entry_path.suffix[1:]
				if extension == "delta" or extension == "filter":
					try:
						with open(entry_path, "rb") as f:
							filter_bytes = f.read()
						filters.append(Filter.from_bytes(filter_bytes))
					except Exception as e:
						logging.warning(f"Error loading filter {entry_path}: {e}")

		intermediates_path = db_dir / "crlite.intermediates"
		if not intermediates_path.exists():
			_update_intermediates(db_dir)

		try:
			with open(intermediates_path, "rb") as f:
				intermediates_bytes = f.read()
			intermediates = Intermediates.decode(intermediates_bytes)
		except Exception as e:
			raise CRLiteDBError(f"Error loading intermediates: {e}")

		return CRLiteDB(db_dir, filters, intermediates)

	def check_revocation_x509(self, cert: x509) -> Status:
		if isinstance(cert, x509.Certificate):
			return self.__query(cert)
		else:
			raise ValueError("Certificate is not of the type x509.Certificate")


	def check_revocation_x509_pem(self, cert_pem_data: bytes) -> Status:
		if isinstance(cert_pem_data, bytes):
			return self.__query(x509.load_pem_x509_certificate(cert_pem_data))
		else:
			raise ValueError("Certificate is not a valid byte array")


	def check_revocation_x509_der(self, cert_der_data: bytes) -> Status:
		if isinstance(cert_der_data, bytes):
			return self.__query(x509.load_der_x509_certificate(cert_der_data))
		else:
			raise ValueError("Certificate is not a valid byte array")


	# Modify
	def __query(self, cert: x509.Certificate) -> Status:
		try:

			# According to the TLS BR Subscriber certificate profile, serial numbers range from 0 to 2^159.
			# This needs atleast 160 bits, or 20 bytes. Keeping 24 bytes to avoid unexpected OverflowError
			serial = cert.serial_number.to_bytes(length=24, byteorder='big').lstrip(b'\x00') # Simulate raw serial
			issuer_dn_bytes = cert.issuer.public_bytes(serialization.Encoding.DER)
			issuer_spki_bytes = Intermediates.lookup_issuer_spki(self.intermediates, cert)

			logging.debug(f"Issuer DN: {binascii.hexlify(issuer_dn_bytes).decode()}")
			logging.debug(f"Serial number: {binascii.hexlify(serial).decode()}")
			if issuer_spki_bytes:
				issuer_spki_hash = hashlib.sha256(issuer_spki_bytes).digest()
				logging.debug(f"Issuer SPKI hash: {binascii.hexlify(issuer_spki_hash).decode()}")
			else:
				return Status.NOT_ENROLLED

			if not cert.not_valid_before_utc < datetime.now(timezone.utc) < cert.not_valid_after_utc:
				return Status.EXPIRED

			maybe_good = False
			covered = False
			timestamps = _get_sct_ids_and_timestamps(cert)

			if issuer_spki_hash:
				for filter in self.filters:
					status = filter.has(issuer_spki_hash, serial, timestamps)
					if status == PyCRLiteStatus.Revoked:
						return Status.REVOKED
					elif status == PyCRLiteStatus.Good:
						maybe_good = True
					elif status == PyCRLiteStatus.NotEnrolled:
						covered = True

			if maybe_good:
				return Status.GOOD
			if covered:
				return Status.NOT_ENROLLED
			return Status.NOT_COVERED

		except Exception as e:
			raise CRLiteDBError(f"Error querying certificate: {e}")


def _get_sct_ids_and_timestamps(cert: x509.Certificate) -> List[Tuple[bytes, int]]:
	try:
		# cert = x509.load_der_x509_certificate(cert_bytes)
		sct_extension = cert.extensions.get_extension_for_oid(x509.ObjectIdentifier(OID_SCT_EXTENSION))
		scts_and_ts = []
		if sct_extension:
			for scts in sct_extension.value:
				log_id = scts.log_id

				#!!! Ensure that the timestamp value returned is the same.
				# The datetime object in the SCT are not timezone aware. We need to manually
				# set the timezone to UTC to get the correct Unix time at the end
				ts = scts.timestamp.replace(tzinfo=timezone.utc)
				ts_unix = int(ts.timestamp()*1000)
				scts_and_ts.append((log_id, ts_unix))

			return scts_and_ts
		else:
			return []

	except Exception as e:
		logging.warning(f"Error parsing certificate for SCTs: {e}")
		return []


def load_crlite_db(db_dir: Union[str, Path], update: bool = True, channel: CRLiteFilterChannel = CRLiteFilterChannel.Default) -> CRLiteDB:
	"""Loads CRLite filters from a directory. If update is set to True, also updates the filter files"""

	if isinstance(db_dir, str):
		db_dir = Path(db_dir)
	elif not isinstance(db_dir, Path):
		raise TypeError("db_dir must be a string or a pathlib.Path object.")

	if not os.path.isdir(db_dir):
		raise FileNotFoundError(f"No such directory: {db_dir}")

	if not isinstance(channel, CRLiteFilterChannel):
		raise TypeError("channel must be an Enum of type crlite_python.CRLiteFilterChannel.")
	if channel == CRLiteFilterChannel.ExpermentalDeltas:
		raise CRLiteDBError("Experiemental Deltas are unsupported")

	if update:
		_update_db(db_dir=db_dir, attachment_url=PROD_ATTACH_URL, base_url=PROD_URL, channel=channel)

	return CRLiteDB.load(db_dir=db_dir)


