#pragma once

#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <string>
#include <vector>
#include "eigen_nn.h"
#include "libtorch_nn.h"

const int repeat_total = 10;

// ==============================
// 2. CSV helper function: Read selected columns
//    Reads data from a CSV file (skips header row) and extracts specified columns.
//    'cols' specifies column indices to read. Reads up to 'num_rows' rows.
//    Returns a 2D vector: each inner vector is one sample, in file order.
// ==============================
inline std::vector<std::vector<double>> read_csv_selected_columns(
	const std::string& filename,
	const std::vector<int>& cols,
	size_t num_rows) {
	std::vector<std::vector<double>> data;
	std::ifstream infile(filename);
	if (!infile.is_open()) {
		std::cerr << "Failed to open file: " << filename << std::endl;
		return data;
	}
	std::string line;
	// Skip header line
	if (!std::getline(infile, line)) {
		std::cerr << "Empty file: " << filename << std::endl;
		return data;
	}
	size_t count = 0;
	while (std::getline(infile, line) && count < num_rows) {
		std::stringstream ss(line);
		std::string cell;
		std::vector<std::string> tokens;
		while (std::getline(ss, cell, ',')) {
			tokens.push_back(cell);
		}
		std::vector<double> selected;
		for (int idx : cols) {
			if (idx < static_cast<int>(tokens.size())) {
				try {
					selected.push_back(std::stod(tokens[idx]));
				}
				catch (const std::exception&) {
					// On parse error, append zero
					selected.push_back(0.0);
				}
			}
			else {
				// If column index out of range, append zero
				selected.push_back(0.0);
			}
		}
		data.push_back(selected);
		++count;
	}
	infile.close();
	return data;
}

// ==============================
// 3. Horizontal concatenation helper: Concatenate two matrices side-by-side
//    Assumes the same number of rows in A and B.
// ==============================
inline std::vector<std::vector<double>> hstack(
	const std::vector<std::vector<double>>& A,
	const std::vector<std::vector<double>>& B) {
	std::vector<std::vector<double>> result;
	if (A.size() != B.size()) {
		std::cerr << "Matrix row counts do not match, cannot concatenate!" << std::endl;
		return result;
	}
	result.reserve(A.size());
	for (size_t i = 0; i < A.size(); ++i) {
		std::vector<double> row = A[i];
		row.insert(row.end(), B[i].begin(), B[i].end());
		result.push_back(std::move(row));
	}
	return result;
}

// ==============================
// 4. File5 processing: Split a specific column into cosine and sine components
//    For Option 8: from file5 selected columns, the third element (index 2)
//    corresponds to global feature 53 (local 5). Replace that element with two
//    new columns: cos(value) and sin(value).
// ==============================
inline void process_file5_split(std::vector<std::vector<double>>& data) {
	for (auto& row : data) {
		if (row.size() < 3) continue;
		double val = row[2]; // corresponds to global feature 53
		double cos_val = std::cos(val);
		double sin_val = std::sin(val);
		// Remove the original value
		row.erase(row.begin() + 2);
		// Insert cosine and sine in place of the original column
		row.insert(row.begin() + 2, sin_val);
		row.insert(row.begin() + 2, cos_val);
	}
}


void test_processed_data(const int type, std::vector<std::vector<double>> input_data_matrix, torch::Tensor X_mean_tensor, torch::Tensor X_scale_tensor, torch::Tensor Y_mean_tensor, torch::Tensor Y_scale_tensor, torch::jit::script::Module module)
{
	// -------------------------------
	// Test using direct NN inputs
	// -------------------------------
	{
		std::vector<double> rv_predictions = fast_predict_vector(
			input_data_matrix,
			X_mean_tensor, X_scale_tensor,
			Y_mean_tensor, Y_scale_tensor,
			module, type);

		// Original flow: inference using TorchScript model (for reference only)
		std::cout << "First 10 denormalized predictions from original flow:" << std::endl;
		for (int i = 0; i < 10; ++i) {
			std::cout << rv_predictions[i] << std::endl;
		}

		std::ofstream outfile("predictions_original.csv");
		if (outfile.is_open()) {
			for (double val : rv_predictions) {
				outfile << val << "\n";
			}
			outfile.close();
			std::cout << "All predictions written to predictions_original.csv" << std::endl;
		}
		else {
			std::cerr << "Failed to write predictions_original.csv" << std::endl;
		}

		// -------------------------------
		// New timing test: NN direct prediction
		// (1) Single-sample test
		// -------------------------------
		{
			const int iterations = input_data_matrix.size();
			auto start_t = std::chrono::steady_clock::now();
			for (int repeat = 0; repeat < repeat_total; repeat++)
			{
				for (int i = 0; i < iterations; ++i) {
					volatile double out = fast_predict_vector(
						input_data_matrix[i], X_mean_tensor, X_scale_tensor,
						Y_mean_tensor, Y_scale_tensor,
						module, type);
					(void)out;
				}
			}
			auto end_t = std::chrono::steady_clock::now();
			double duration_t = std::chrono::duration_cast<std::chrono::milliseconds>(end_t - start_t).count() / 1000.0;
			std::cout << "fast_predict_vector single-sample 100k calls took: "
				<< duration_t << " s; " << duration_t / 60.0 << " mins; " << duration_t / 3600.0 << " hours" << std::endl;
		}

		// (2) Batch test: construct 100k rows of same sample
		// -------------------------------
		{
			std::vector<std::vector<double>> batch_rv = input_data_matrix;
			auto start_t = std::chrono::steady_clock::now();
			for (int repeat = 0; repeat < repeat_total; repeat++)
			{
				std::vector<double> batch_rv_out = fast_predict_vector(
					batch_rv, X_mean_tensor, X_scale_tensor,
					Y_mean_tensor, Y_scale_tensor,
					module, type);
			}
			auto end_t = std::chrono::steady_clock::now();
			double duration_t = std::chrono::duration_cast<std::chrono::milliseconds>(end_t - start_t).count() / 1000.0;
			std::cout << "fast_predict_vector batch 100k RV samples took: "
				<< duration_t << " s; " << duration_t / 60.0 << " mins; " << duration_t / 3600.0 << " hours" << std::endl;
		}
	}
}

void test_raw_data(const int type, std::vector<std::vector<double>> file2_data, torch::Tensor X_mean_tensor, torch::Tensor X_scale_tensor, torch::Tensor Y_mean_tensor, torch::Tensor Y_scale_tensor, torch::jit::script::Module module)
{
	{
		// Use fast_predict_vector_raw_data interface (type=1 uses nn_input_1_rotate_lambert)
		std::vector<double> rv_predictions = fast_predict_vector_raw_data(
			file2_data,
			X_mean_tensor, X_scale_tensor,
			Y_mean_tensor, Y_scale_tensor,
			module, type);
		std::cout << "First 10 raw RV predictions:" << std::endl;
		for (int i = 0; i < std::min((int)rv_predictions.size(), 10); ++i) {
			std::cout << rv_predictions[i] << std::endl;
		}

		std::ofstream rv_outfile("predictions_raw_rv.csv");
		if (rv_outfile.is_open()) {
			for (double val : rv_predictions) {
				rv_outfile << val << "\n";
			}
			rv_outfile.close();
			std::cout << "Raw RV predictions written to predictions_raw_rv.csv" << std::endl;
		}
		else {
			std::cerr << "Failed to write predictions_raw_rv.csv" << std::endl;
		}
	}
	// -------------------------------
	// New timing test: raw RV prediction
	// (1) Single-sample test (fast_predict_vector overload)
	// -------------------------------
	{
		const int iterations = file2_data.size();
		auto start_t = std::chrono::steady_clock::now();
		for (int repeat = 0; repeat < repeat_total; repeat++)
		{
			for (int i = 0; i < iterations; ++i) {
				volatile double out = fast_predict_vector_raw_data(
					file2_data[i], X_mean_tensor, X_scale_tensor,
					Y_mean_tensor, Y_scale_tensor,
					module, type);
				(void)out;
			}
		}
		auto end_t = std::chrono::steady_clock::now();
		double duration_t = std::chrono::duration_cast<std::chrono::milliseconds>(end_t - start_t).count() / 1000.0;
		std::cout << "fast_predict_vector_raw_data single-sample 100k calls took: "
			<< duration_t << " s; " << duration_t / 60.0 << " mins; " << duration_t / 3600.0 << " hours" << std::endl;
	}

	// (2) Batch test: construct 100k rows of same sample
	// -------------------------------
	{
		std::vector<std::vector<double>> batch_rv = file2_data;
		auto start_t = std::chrono::steady_clock::now();
		for (int repeat = 0; repeat < repeat_total; repeat++)
		{
			std::vector<double> batch_rv_out = fast_predict_vector_raw_data(
				batch_rv, X_mean_tensor, X_scale_tensor,
				Y_mean_tensor, Y_scale_tensor,
				module, type);
		}
		auto end_t = std::chrono::steady_clock::now();
		double duration_t = std::chrono::duration_cast<std::chrono::milliseconds>(end_t - start_t).count() / 1000.0;
		std::cout << "fast_predict_vector_raw_state batch 100k RV samples took: "
			<< duration_t << " s; " << duration_t / 60.0 << " mins; " << duration_t / 3600.0 << " hours" << std::endl;
	}
}

void test_nn_model(size_t num_test_rows,
                   std::string base_path,
                   std::string suffix,
                   std::string libtorch_model_path,
                   std::string eigen_model_path,
                   const int type = 1)
{
    // For Option 8: use file5 (data_feasible_lambert_dv.csv) and file7 (data_feasible_misc_dv.csv)
    std::string file5_path = base_path + "/data_feasible_lambert" + suffix + ".csv";
    std::string file7_path = base_path + "/data_feasible_misc" + suffix + ".csv";
    // Select global columns 48,49,53,60,61,63,64,66,67,69,70,72,73 from file5 (local indices {0,1,5,12,13,15,16,18,19,21,22,24,25})
    std::vector<int> file5_cols = { 0, 1, 5, 12, 13, 15, 16, 18, 19, 21, 22, 24, 25 };
    // Select global columns 82,83,85 from file7 (local indices {0,1,3})
    std::vector<int> file7_cols = { 0, 1, 3 };
    std::vector<int> file7_cols_new = { 0, 1, 2, 3 };

    // -------------------------------
    // Read CSV data and assemble inputs
    // -------------------------------
    auto file5_data = read_csv_selected_columns(file5_path, file5_cols, num_test_rows);
    if (file5_data.empty()) {
        std::cerr << "Failed to read data from " << file5_path << std::endl;
        return;
    }
    process_file5_split(file5_data);  // After splitting, each row changes from 13 cols to 14 cols

    auto file7_data = read_csv_selected_columns(file7_path, file7_cols, num_test_rows);
    if (file7_data.empty()) {
        std::cerr << "Failed to read data from " << file7_path << std::endl;
        return;
    }

    auto input_data_matrix = hstack(file5_data, file7_data);  // Final input dimension: 17
    // Append bias term
    for (auto& row : input_data_matrix) {
        row.push_back(1.32712440018e20);
    }

	for (auto& row : input_data_matrix) {
		row[15] = 0.1 / row[15];
	}

    size_t final_cols = input_data_matrix[0].size();
    std::cout << "Assembled input data: " << input_data_matrix.size()
        << " rows, " << final_cols << " cols" << std::endl;


    // -------------------------------
    // Test predictions using raw RV data and NN input mapping
    // -------------------------------
    
	// Read raw RV data: file2 (indices 0-11)
	std::string file2_path = base_path + "/data_feasible_rv_inertial" + suffix + ".csv";
	std::vector<int> file2_cols;
	for (int i = 0; i < 12; ++i) {
		file2_cols.push_back(i);
	}
	auto file2_data = read_csv_selected_columns(file2_path, file2_cols, num_test_rows);
	if (file2_data.empty()) {
		std::cerr << "Failed to read data from " << file2_path << std::endl;
		return;
	}

	auto file7_data_new = read_csv_selected_columns(file7_path, file7_cols_new, num_test_rows);
	if (file7_data_new.empty()) {
		std::cerr << "Failed to read data from " << file7_path << std::endl;
		return;
	}
	auto input_data_matri2x = hstack(file2_data, file7_data_new);  // Final input dimension: 17

	file2_data = input_data_matri2x;
	for (auto& row : file2_data) {
		row.push_back(1.32712440018e20);
	}
	std::cout << "Assembled input data: " << file2_data.size()
		<< " rows, " << final_cols << " cols" << std::endl;
	// Test Eigen predictor performance
	{
		// Note: set number of network layers + 1
		int layers = 9 + 1;
		EigenFastPredictor_small predictor(eigen_model_path, layers);
		double out;
		if (type == 1) {
			out = predictor.fast_predict_vector(input_data_matrix[0]);
		}
		else {
			out = predictor.fast_predict_vector_tmin(input_data_matrix[0]);
		}
		std::cout << "EIGEN predicted first result: " << out << std::endl;

		auto start_t = std::chrono::steady_clock::now();
		for(int repeat =0; repeat < repeat_total; repeat++)
		{
			std::vector<std::vector<double>> map_data(file2_data.size());
			for (size_t i = 0; i < file2_data.size(); ++i) {
				map_data[i] = nn_input_1_rotate_lambert(file2_data[i]);
			}
			for (int i = 0; i < map_data.size(); ++i) {
				double out_loop;
				if (type == 1) {
					out_loop = predictor.fast_predict_vector(map_data[i]);
				}
				else {
					out_loop = predictor.fast_predict_vector_tmin(map_data[i]);
				}
				volatile double dummy = out_loop;
			}

		}
		auto end_t = std::chrono::steady_clock::now();
		double duration_t = std::chrono::duration_cast<std::chrono::milliseconds>(end_t - start_t).count() / 1000.0;
		std::cout << "fast_predict_vector_raw_data (100k calls on single RV sample with EIGEN) took: "
			<< duration_t << " s; " << duration_t / 60.0 << " mins; " << duration_t / 3600.0 << " hours" << std::endl;
	}

	{
		// Note: set number of network layers + 1 (default constructor)
		EigenFastPredictor predictor(eigen_model_path);
		double out;
		std::vector<double> map_1 = nn_input_1_rotate_lambert(file2_data[0]);
		if (type == 1) {
			out = predictor.fast_predict_vector(map_1);
		}
		else {
			out = predictor.fast_predict_vector_tmin(map_1);
		}
		std::cout << "EIGEN predicted first result: " << out << std::endl;

		// Map inputs via nn_input_1_rotate_lambert
		auto start_t = std::chrono::steady_clock::now();
		for (int repeat = 0; repeat < repeat_total; repeat++)
		{
			std::vector<std::vector<double>> map_data(file2_data.size());
			for (size_t i = 0; i < file2_data.size(); ++i) {
				map_data[i] = nn_input_1_rotate_lambert(file2_data[i]);
			}
			for (int i = 0; i < map_data.size(); ++i) {
				double out_loop;
				if (type == 1) {
					out_loop = predictor.fast_predict_vector(map_data[i]);
				}
				else {
					out_loop = predictor.fast_predict_vector_tmin(map_data[i]);
				}
				volatile double dummy = out_loop;
			}
		}
		auto end_t = std::chrono::steady_clock::now();
		double duration_t = std::chrono::duration_cast<std::chrono::milliseconds>(end_t - start_t).count() / 1000.0;
		std::cout << "fast_predict_vector_raw_data mapped (100k calls) took: "
			<< duration_t << " s; " << duration_t / 60.0 << " mins; " << duration_t / 3600.0 << " hours" << std::endl;
	}



	// -------------------------------
	// Normalize input data: load scaler_X.csv (expects 17 rows of mean and scale)
	// -------------------------------
	std::string scalerX_csv = libtorch_model_path + "/scaler_X.csv";
	auto scalerX = read_scaler_csv(scalerX_csv);
	std::vector<double> X_means = scalerX.first;
	std::vector<double> X_scales = scalerX.second;
	final_cols = X_scales.size();

	if (X_means.size() != final_cols || X_scales.size() != final_cols) {
		std::cerr << "Number of scaler_X parameters (" << X_means.size()
			<< ") does not match number of input features (" << final_cols << ")!" << std::endl;
		return;
	}
	torch::Tensor X_mean_tensor = torch::from_blob(X_means.data(), { (long)final_cols }, torch::kFloat64)
		.to(torch::kFloat32)
		.unsqueeze(0)
		.clone();
	torch::Tensor X_scale_tensor = torch::from_blob(X_scales.data(), { (long)final_cols }, torch::kFloat64)
		.to(torch::kFloat32)
		.unsqueeze(0)
		.clone();

	// Load Y scaler
	std::string scalerY_csv = libtorch_model_path + "/scaler_Y.csv";
	auto scalerY = read_scaler_csv(scalerY_csv);
	std::vector<double> Y_means = scalerY.first;
	std::vector<double> Y_scales = scalerY.second;
	if (Y_means.size() != 1 || Y_scales.size() != 1) {
		std::cerr << "Scaler_Y parameter count is not 1!" << std::endl;
		return;
	}
	torch::Tensor Y_mean_tensor = torch::tensor(Y_means[0], torch::kFloat32);
	torch::Tensor Y_scale_tensor = torch::tensor(Y_scales[0], torch::kFloat32);

	// -------------------------------
	// Load TorchScript model (17-dim input, 1-dim output)
	// -------------------------------
	std::string model_file = libtorch_model_path + "/model_cpu.pt";
	torch::jit::script::Module module;
	try {
		module = torch::jit::load(model_file);
	}
	catch (const c10::Error& e) {
		std::cerr << "Failed to load model: " << model_file << std::endl;
		return;
	}
	module.eval();
	std::cout << "Model loaded successfully!" << std::endl;

	torch::NoGradGuard no_grad;

	test_raw_data(type, file2_data, X_mean_tensor, X_scale_tensor, Y_mean_tensor, Y_scale_tensor, module);


    test_processed_data(type, input_data_matrix, X_mean_tensor, X_scale_tensor, Y_mean_tensor, Y_scale_tensor, module);
}
