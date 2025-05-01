use anyhow::anyhow;
use crate::Ome;
use crate::ome::{
    Convert, UnitsElectricPotential, UnitsFrequency, UnitsLength, UnitsPower,
    UnitsPressure, UnitsTemperature, UnitsTime,
};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::IntoPyObjectExt;

/// helper class to be used for unpickling
#[pyclass(module = "ome_metadata.ome_metadata_rs")]
struct Constructor;

#[pymethods]
impl Constructor {
    #[new]
    fn new() -> Self {
        Self
    }

    fn __getstate__(&self) -> (u8,) {
        (0,)
    }

    fn __setstate__(&self, _state: (u8,)) {}

    #[staticmethod]
    fn __call__(py: Python, class: String, variant: String) -> PyResult<Bound<PyAny>> {
        match class.as_str() {
            "ElectricPotential" => ElectricPotential::new(&variant)?.into_bound_py_any(py),
            "Frequency" => Frequency::new(&variant)?.into_bound_py_any(py),
            "Length" => Length::new(&variant)?.into_bound_py_any(py),
            "Power" => Power::new(&variant)?.into_bound_py_any(py),
            "Pressure" => Pressure::new(&variant)?.into_bound_py_any(py),
            "Temperature" => Temperature::new(&variant)?.into_bound_py_any(py),
            "Time" => Time::new(&variant)?.into_bound_py_any(py),
            _ => Err(anyhow!("cannot parse class {}", class).into())
        }
    }
}

macro_rules! impl_enum_into_py_object {
    ($($s:ident: $t:ty $(,)?)*) => {
        $(
            #[pyclass(module = "ome_metadata.ome_metadata_rs")]
            pub struct $s {
                inner: $t,
            }

            #[pymethods]
            impl $s {
                #[new]
                fn new(unit: &str) -> PyResult<Self> {
                    match unit.parse() {
                        Ok(unit) => Ok(Self { inner: unit }),
                        Err(_) => Err(PyErr::new::<PyValueError, _>(format!("Invalid unit: {}", unit)))
                    }
                }

                /// convert a value between units
                fn convert(&self, unit: &str, value: f64) -> PyResult<f64> {
                    match unit.parse() {
                        Ok(unit) => Ok(self.inner.convert(&unit, value)?),
                        Err(_) => Err(PyErr::new::<PyValueError, _>(format!("Invalid unit: {}", unit)))
                    }
                }

                /// all possible variants of this enum that can be constructed or converted into
                #[staticmethod]
                fn variants() -> Vec<String> {
                    <$t>::variants().iter().map(|v| format!("{:?}", v)).collect()
                }

                fn __repr__(&self) -> String {
                    format!("{:?}", self.inner)
                }

                fn __str__(&self) -> String {
                    format!("{:?}", self.inner)
                }

                fn __reduce__(&self) -> PyResult<(Constructor, (String, String))> {
                    Ok((Constructor, (stringify!($s).to_string(), format!("{:?}", self.inner))))
                }
            }

            impl<'py> IntoPyObject<'py> for $t {
                type Target = $s;
                type Output = Bound<'py, Self::Target>;
                type Error = PyErr;
                fn into_pyobject(self, py: Python<'py>) -> PyResult<Self::Output> {
                    Bound::new(py, $s { inner: self })
                }
            }
        )*
    };
}

impl_enum_into_py_object! {
    ElectricPotential: UnitsElectricPotential
    Frequency: UnitsFrequency
    Length: UnitsLength
    Power: UnitsPower
    Pressure: UnitsPressure
    Temperature: UnitsTemperature
    Time: UnitsTime
}

#[pymodule]
#[pyo3(name = "ome_metadata_rs")]
fn ome_metadata_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Constructor>()?;
    m.add_class::<ElectricPotential>()?;
    m.add_class::<Frequency>()?;
    m.add_class::<Length>()?;
    m.add_class::<Power>()?;
    m.add_class::<Pressure>()?;
    m.add_class::<Temperature>()?;
    m.add_class::<Time>()?;

    #[pyfn(m)]
    fn ome(text: &str) -> PyResult<Ome> {
        Ok(text.parse()?)
    }

    Ok(())
}
