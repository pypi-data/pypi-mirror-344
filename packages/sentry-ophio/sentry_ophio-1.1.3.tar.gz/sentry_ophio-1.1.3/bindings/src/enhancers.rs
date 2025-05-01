//! Python bindings for the enhancers module.
//!
//! See `enhancers.pyi` for documentation on classes and functions.

use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use pyo3::types::PyList;
use rust_ophio::enhancers;

#[derive(FromPyObject)]
#[pyo3(from_item_all)]
pub struct Frame {
    category: OptStr,
    family: OptStr,
    function: OptStr,
    module: OptStr,
    package: OptStr,
    path: OptStr,
    in_app: Option<bool>,
    orig_in_app: Option<i8>,
}

struct OptStr(Option<enhancers::StringField>);

impl FromPyObject<'_> for OptStr {
    fn extract_bound(ob: &Bound<'_, PyAny>) -> PyResult<Self> {
        if ob.is_none() {
            return Ok(Self(None));
        }
        let s: &[u8] = ob.extract()?;
        let s = std::str::from_utf8(s)?;
        Ok(Self(Some(enhancers::StringField::new(s))))
    }
}

#[pyclass]
pub struct AssembleResult {
    #[pyo3(get)]
    contributes: bool,
    #[pyo3(get)]
    hint: Option<String>,
    #[pyo3(get)]
    invert_stacktrace: bool,
}

#[pyclass]
pub struct Component {
    #[pyo3(get, set)]
    contributes: Option<bool>,
    #[pyo3(get)]
    hint: Option<String>,
}

#[pymethods]
impl Component {
    #[new]
    #[pyo3(signature = (contributes=None))]
    fn new(contributes: Option<bool>) -> Self {
        Self {
            contributes,
            hint: None,
        }
    }
}

#[derive(FromPyObject)]
#[pyo3(from_item_all)]
pub struct ExceptionData {
    ty: OptStr,
    value: OptStr,
    mechanism: OptStr,
}

#[pyclass]
pub struct Cache(enhancers::Cache);

#[pymethods]
impl Cache {
    #[new]
    fn new(size: usize) -> PyResult<Self> {
        Ok(Self(enhancers::Cache::new(size)))
    }
}

#[pyclass]
pub struct Enhancements(enhancers::Enhancements);

#[pymethods]
impl Enhancements {
    #[staticmethod]
    fn empty() -> Self {
        Self(enhancers::Enhancements::default())
    }

    #[staticmethod]
    fn parse(input: &str, cache: &mut Cache) -> PyResult<Self> {
        let inner = enhancers::Enhancements::parse(input, &mut cache.0).map_err(pretty_error)?;
        Ok(Self(inner))
    }

    #[staticmethod]
    fn from_config_structure(input: &[u8], cache: &mut Cache) -> PyResult<Self> {
        let inner = enhancers::Enhancements::from_config_structure(input, &mut cache.0)
            .map_err(pretty_error)?;
        Ok(Self(inner))
    }

    fn extend_from(&mut self, other: &Self) {
        self.0.extend_from(&other.0)
    }

    fn apply_modifications_to_frames(
        &self,
        py: Python,
        frames: Bound<'_, PyList>,
        exception_data: ExceptionData,
    ) -> PyResult<Vec<PyObject>> {
        let mut frames: Vec<_> = frames
            .into_iter()
            .map(convert_frame_from_py)
            .collect::<PyResult<_>>()?;

        let exception_data = enhancers::ExceptionData {
            ty: exception_data.ty.0,
            value: exception_data.value.0,
            mechanism: exception_data.mechanism.0,
        };

        self.0
            .apply_modifications_to_frames(&mut frames, &exception_data);

        frames
            .into_iter()
            .map(|f| {
                (f.category.as_ref().map(|c| c.as_str()), f.in_app)
                    .into_pyobject(py)
                    .map(Into::into)
            })
            .collect()
    }

    fn assemble_stacktrace_component(
        &self,
        frames: Bound<'_, PyList>,
        exception_data: ExceptionData,
        mut grouping_components: Vec<PyRefMut<Component>>,
    ) -> PyResult<AssembleResult> {
        let frames: Vec<_> = frames
            .into_iter()
            .map(convert_frame_from_py)
            .collect::<PyResult<_>>()?;

        let exception_data = enhancers::ExceptionData {
            ty: exception_data.ty.0,
            value: exception_data.value.0,
            mechanism: exception_data.mechanism.0,
        };

        let mut components: Vec<_> = grouping_components
            .iter()
            .map(|c| convert_component_from_py(c))
            .collect();

        let assemble_result =
            self.0
                .assemble_stacktrace_component(&mut components, &frames, &exception_data);

        for (py_component, rust_component) in
            grouping_components.iter_mut().zip(components.into_iter())
        {
            py_component.contributes = rust_component.contributes;
            py_component.hint = rust_component.hint;
        }

        Ok(AssembleResult {
            contributes: assemble_result.contributes,
            hint: assemble_result.hint,
            invert_stacktrace: assemble_result.invert_stacktrace,
        })
    }
}

fn pretty_error(err: anyhow::Error) -> PyErr {
    use std::fmt::Write;
    let mut err_str = format!(
        "Invalid syntax {err}{}",
        if err.source().is_some() { ":" } else { "" }
    );

    let mut source = err.source();
    while let Some(err) = source {
        write!(&mut err_str, "\n{err}").unwrap();
        source = err.source();
    }

    PyRuntimeError::new_err(err_str)
}

fn convert_frame_from_py(frame: Bound<'_, PyAny>) -> PyResult<enhancers::Frame> {
    let frame: Frame = frame.extract()?;
    let frame = enhancers::Frame {
        category: frame.category.0,
        family: enhancers::Families::new(frame.family.0.as_deref().unwrap_or("other")),
        function: frame.function.0,
        module: frame.module.0,
        package: frame.package.0,
        path: frame.path.0,

        in_app: frame.in_app,
        orig_in_app: frame.orig_in_app.map(|in_app| match in_app {
            0 => Some(false),
            1 => Some(true),
            _ => None,
        }),
    };
    Ok(frame)
}

fn convert_component_from_py(component: &Component) -> enhancers::Component {
    enhancers::Component {
        contributes: component.contributes,
        hint: None,
    }
}
