#include <pybind11/pybind11.h>
#include <pybind11/stl.h>      // std::vector ⇄ list
#include <pybind11/eigen.h>    // 如果你想直接传 Eigen::VectorXd
#include "eigen_nn.h"

namespace py = pybind11;

PYBIND11_MODULE(nn_lowthrust, m) {           // Python import lowthrust
    m.doc() = "Eigen-based low-thrust predictor (pybind11)";

    /* -- 绑定类 ---------------------------------------------------------- */
    py::class_<EigenFastPredictor>(m, "EigenFastPredictor")
        .def(py::init<const std::string&>(),
            py::arg("model_dir"))
        .def("fast_predict_vector",
            &EigenFastPredictor::fast_predict_vector,
            py::arg("x"))
        .def("fast_predict_vector_tmin",
            &EigenFastPredictor::fast_predict_vector_tmin,
            py::arg("x"));

    /* -- 绑定自由函数 ---------------------------------------------------- */
    m.def("nn_input_1_rotate_lambert",
        &nn_input_1_rotate_lambert,
        py::arg("in"),
        "Pre-process inputs exactly like the C++ helper");
}
