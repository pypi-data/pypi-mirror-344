use pyo3::prelude::*;
use pyo3::types::PyBytes;
use std::collections::HashMap;
use clubcard_crlite::{CRLiteClubcard, CRLiteKey, CRLiteStatus};

type IssuerDN = Vec<u8>;
type DERCert = Vec<u8>;

mod exceptions {
    pyo3::import_exception!(exceptions, CRLiteDBError);
}

#[pyclass(module = "crlite_python_rs", get_all)]
pub struct Intermediates {
    intermediates: HashMap<IssuerDN, Vec<DERCert>>,
}

#[pymethods]
impl Intermediates {
    #[new]
    fn __new__() -> Self {
        Intermediates {
            intermediates: HashMap::new(),
        }
    }

    // This function will be called from Python to populate the Intermediates struct.
    // m: &Bound<'_, PyModule>
    fn add_cert(&mut self, issuer_dn: &Bound<'_, PyBytes>, der_cert: &Bound<'_, PyBytes>) {
        let issuer_dn_vec = issuer_dn.as_bytes().to_vec();
        let der_cert_vec = der_cert.as_bytes().to_vec();
        self.intermediates.entry(issuer_dn_vec).or_default().push(der_cert_vec);
    }

    fn to_bincode(&self) -> PyResult<Vec<u8>> {
        let encoded = bincode::serialize(&self.intermediates)
            .map_err(|e| exceptions::CRLiteDBError::new_err(format!("Failed to serialize: {}", e)))?;
        Ok(encoded)
    }

    #[staticmethod]
    fn from_bincode(bytes: &Bound<'_, PyBytes>) -> PyResult<Self> {
        let bytes_ref = bytes.as_ref();
        let bytes_slice = bytes_ref.extract::<&[u8]>()?;

        let intermediates: HashMap<IssuerDN, Vec<DERCert>> =
            bincode::deserialize(bytes_slice)
                .map_err(|e| exceptions::CRLiteDBError::new_err(format!("Failed to deserialize: {}", e)))?;
        Ok(Intermediates { intermediates })
    }
}

// Wrap the CRLiteStatus enum for Python
#[pyclass(module = "crlite_python_rs", eq, eq_int)]
// #[pyclass(eq, eq_int)]
#[derive(PartialEq)]
pub enum PyCRLiteStatus {
    Good,
    NotCovered,
    NotEnrolled,
    Revoked,
}

// Convert between the Rust and Python versions of CRLiteStatus
impl From<CRLiteStatus> for PyCRLiteStatus {
    fn from(status: CRLiteStatus) -> Self {
        match status {
            CRLiteStatus::Good => PyCRLiteStatus::Good,
            CRLiteStatus::NotCovered => PyCRLiteStatus::NotCovered,
            CRLiteStatus::NotEnrolled => PyCRLiteStatus::NotEnrolled,
            CRLiteStatus::Revoked => PyCRLiteStatus::Revoked,
        }
    }
}

#[pyclass(module = "crlite_python_rs")]
pub struct PyCRLiteClubcard {
    clubcard: CRLiteClubcard,
}

type LogId = [u8; 32];

#[pymethods]
impl PyCRLiteClubcard {
    // Add a __str__ or __repr__ method to leverage the Display impl
    fn __str__(&self) -> PyResult<String> {
        Ok(format!("{}", self.clubcard))
    }

    #[staticmethod] // Or #[classmethod] if you need access to the class object
    fn load_filter(filter_bytes: Vec<u8>) -> PyResult<Self> {

        // Call the Rust from_bytes method
        let clubcard = CRLiteClubcard::from_bytes(&filter_bytes)
        .map_err(|_| exceptions::CRLiteDBError::new_err(format!("Could not load filter")))?; // Uses the `From<ClubcardError> for PyErr` impl

        // Wrap the Rust object in our PyO3 struct and return it
        Ok(PyCRLiteClubcard { clubcard: clubcard })
    }

    #[staticmethod]
    fn query_filter(
        filter: &PyCRLiteClubcard,
        issuer_spki_hash: &[u8],
        serial: &[u8],
        py_timestamps: Vec<(Vec<u8>, u64)>,
    ) -> PyResult<PyCRLiteStatus> {

        let crlite_key = CRLiteKey::new(issuer_spki_hash.try_into().unwrap(), serial);
        let mut validated_timestamps: Vec<(&[u8; 32], u64)> = Vec::with_capacity(py_timestamps.len());

        for (log_id_vec, ts) in &py_timestamps {
            // Validate each log ID length (must be 32 bytes)
            let log_id_slice: &[u8; 32] = log_id_vec
                .as_slice() // Get &[u8] from Vec<u8>
                .try_into() // Try to convert &[u8] to &[u8; 32]
                .map_err(|_| exceptions::CRLiteDBError::new_err("Each log ID in timestamps must be exactly 32 bytes"))?;

            // Push the validated reference and the timestamp into the temporary vector
            validated_timestamps.push((log_id_slice, *ts));
        }
        let status = filter.clubcard.contains(
            &crlite_key, // &CRLiteKey
            // Convert the temporary Vec into an iterator
            validated_timestamps.into_iter().map(|(log_id_ref, ts)| {
                 // Map from (&[u8; 32], u64) to (&LogId, Timestamp)
                 // Since LogId is [u8; 32], `log_id_ref` already has the type `&[u8; 32]`.
                 // If LogId is a struct wrapping [u8; 32], you might need unsafe code
                 // or a different approach to get a reference to the inner [u8; 32]
                 // *or* redesign LogId/CRLiteKey to hold owned data or smart pointers.
                 // Assuming LogId is a type alias for [u8; 32]:
                 (log_id_ref as &LogId, ts) // Cast &[u8; 32] to &LogId (trivial if alias)
             })
        );

        // Matching the status type here instead of type conversion due to weird equality comparision issues
        let py_status = match status {
            CRLiteStatus::Good => PyCRLiteStatus::Good,
            CRLiteStatus::NotCovered => PyCRLiteStatus::NotCovered,
            CRLiteStatus::NotEnrolled => PyCRLiteStatus::NotEnrolled,
            CRLiteStatus::Revoked => PyCRLiteStatus::Revoked,
        };
        Ok(py_status)
        // Ok(status.into())
    }

}


#[pymodule]
#[pyo3(name="_internal")]
fn crlite_python_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyCRLiteStatus>()?;
    m.add_class::<Intermediates>()?;
    m.add_class::<PyCRLiteClubcard>()?;
    Ok(())
}