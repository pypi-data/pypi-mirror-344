use pyo3::prelude::*;

#[pyfunction]
fn moyenne(a: f64, b: f64) -> PyResult<f64> {
    Ok((a + b) / 2.0)
}


#[pymodule]
fn moyenne_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(moyenne, m)?)
}