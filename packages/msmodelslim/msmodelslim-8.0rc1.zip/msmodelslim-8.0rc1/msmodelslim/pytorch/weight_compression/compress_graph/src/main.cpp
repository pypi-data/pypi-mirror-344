/**
 * Copyright (c) Huawei Technologies Co., Ltd. 2023-2024. All rights reserved.
 * Description: graph_utils.h for weight compression
 * Author: Huawei
 * Create: 2023-09-21
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "graph_utils.h"
#include "ge_ir_build.h"
#include "File.h"

constexpr int NUMBER_12 = 12;

int RunCompressGraph(ge::Session *session, uint8_t* data, vector<int64_t> &shape, vector<int64_t> &compressParameters,
                         vector<string> paths){
  uint32_t compressFc_graph_id = 1;
  Graph compressFcGraph("compressFc Graph");
  // Build graph
  int ret = BuildCompressFcGraph(compressFcGraph, data, shape, compressParameters);
  if (ret != SUCCESS) {
    std::cout << "Generate compressFc Graph failed."<<std::endl;
    return FAILED;
  }

  // Add graph
  ret = session->AddGraph(compressFc_graph_id, compressFcGraph);
  if (ret != SUCCESS) {
    std::cout<<"Session add compressFc Graph failed."<< std::endl;
    return FAILED;
  }
  std::cout<<"Session add compressFc Graph success."<< std::endl;

  std::vector<Tensor> input_mm;
  std::vector<Tensor> output_mm;
  ret = session->RunGraph(compressFc_graph_id, input_mm, output_mm);
  if (ret != SUCCESS) {
    std::cout << "Session run compressFc graph failed." << std::endl;
    return FAILED;
  }

  auto infoData = reinterpret_cast<uint32_t*>(output_mm[2].GetData());

  constexpr uint8_t OUTPUT_WEIGHT_PATH_INDEX = 0;
  constexpr uint8_t INDEX_PATH_INDEX = 1;
  constexpr uint8_t COMPRESS_INFO_PATH_INDEX = 2;
  if (!File::CheckFileBeforeCreateOrWrite(paths[OUTPUT_WEIGHT_PATH_INDEX].c_str(), true)) {
    return FAILED;
  }
  FILE *fp1 = fopen(paths[OUTPUT_WEIGHT_PATH_INDEX].c_str(), "w+");
  fwrite(output_mm[0].GetData(), sizeof(int8_t), infoData[2], fp1);
  fclose(fp1);

  if (!File::CheckFileBeforeCreateOrWrite(paths[INDEX_PATH_INDEX].c_str(), true)) {
    return FAILED;
  }
  FILE *fp2 = fopen(paths[INDEX_PATH_INDEX].c_str(), "w+");
  fwrite(output_mm[1].GetData(), sizeof(uint8_t), output_mm[1].GetSize(), fp2);
  fclose(fp2);

  if (!File::CheckFileBeforeCreateOrWrite(paths[COMPRESS_INFO_PATH_INDEX].c_str(), true)) {
    return FAILED;
  }
  FILE *fp3 = fopen(paths[COMPRESS_INFO_PATH_INDEX].c_str(), "w+");
  fwrite(output_mm[2].GetData(), sizeof(uint32_t), 3, fp3);
  fclose(fp3);
  
  return SUCCESS;
}

int RunSession(uint8_t* data, vector<int64_t> &shape, 
               vector<string> paths, vector<int64_t> &compressParameters)
{
    // System init
  std::map<AscendString, AscendString> config = {{"ge.exec.deviceId", "0"},
                                                 {"ge.graphRunMode", "0"},
                                                 {"ge.exec.precision_mode", "allow_fp32_to_fp16"}};
  
  Status ret = ge::GEInitialize(config);
  if (ret != SUCCESS) {
    std::cout<<"GE initialize failed.\n";
    return FAILED;
  }
  std::cout<<"Initialize ge success."<<std::endl;

  // creat session
  std::map < ge::AscendString, ge::AscendString > options;
  ge::Session *session = new Session(options);
  if (session == nullptr) {
    std::cout << "Create session failed." << std::endl;
    return FAILED;
  }
  std::cout<<"Create session success."<<std::endl;
  
  RunCompressGraph(session, data, shape, compressParameters, paths);

  // destroy session
  delete session;
  session = nullptr;

  // system finalize
  ret = ge::GEFinalize();
  if (ret != SUCCESS) {
    std::cout<<"Finalize ge failed."<<std::endl;
    return FAILED;
  }
  std::cout<<"Finalize ge success."<<std::endl;
  return SUCCESS;
}

bool CheckInputsStollValid(int argc, char* argv[])
{
  if (argc != NUMBER_12) {
    std::cout << "Please check your input params count is 11." << std::endl;
    return false;
  }

  try {
    const int inputStollCount = 7;
    for (int i = 1; i <= inputStollCount; i++) {
      try {
        std::stoll(argv[i]);
      } catch (const std::invalid_argument &e) {
        std::cout << "Invalid argument for param " << i << ". Please check your input params." << std::endl;
        return false;
      } catch (const std::out_of_range &e) {
        std::cout << "Out of range for param " << i << ". Please check your input params." << std::endl;
        return false;
      }
    }
  } catch (...) {
    std::cout << "An unknown error occurred." << std::endl;
    return false;
  }

  return true;
}

int main(int argc, char* argv[])
{
  if (!CheckInputsStollValid(argc, argv)) {
    return FAILED;
  }

  const int64_t dimK = std::stoll(argv[1]);
  const int64_t dimN = std::stoll(argv[2]);
  const int64_t isTight = std::stoll(argv[3]);
  const int64_t k_value = std::stoll(argv[4]);
  const int64_t n_value = std::stoll(argv[5]);
  const int64_t compressType = std::stoll(argv[6]);
  const int64_t isTiling = std::stoll(argv[7]);
  const string inputWeightPath = argv[8];
  const string outputWeightPath = argv[9];
  const string indexPath = argv[10];
  const string compressInfoPath = argv[11];

  vector<string> paths = {outputWeightPath, indexPath, compressInfoPath};
  vector<int64_t> inputWeightShape = {dimK, dimN, 16, 32};
  if (CheckShape(inputWeightShape) == FAILED) {
      std::cout << "Invalid shape. Please check your input dimK(" << dimK << ") dimN(" << dimN << ")." << std::endl;
  }
  uint8_t* data = nullptr;
  int64_t compress_size = 1;
  GetDataSizeFromShape(inputWeightShape, compress_size);
  int64_t tileNumN = (inputWeightShape[1] + 8 - 1)/8;
  int64_t tileNumK = (inputWeightShape[0] + 8 - 1)/8;
  int64_t indexBaseSize = isTight ? 8 : 2;
  int64_t index_size = indexBaseSize * tileNumK * tileNumN;
  /*
   (0)compressed_size, 
   (1)index_size, 
   2)isTight: 1 
   (3)enginnum: 4
   (4)channel: 2
   (5)ratios: 64
   6)k_value: 1 
   7)n_value: 1 
   8)block_dim: 1 
   9)CompressType: 0 
   10)isTiling: 0
  */
  vector<int64_t> compressParameters = {compress_size, index_size, isTight, 4, 2, 64, k_value, n_value, 1, compressType, isTiling};
  try {
    if (!GetDataFromBin(inputWeightPath, inputWeightShape, &data, sizeof(int8_t))) {
      delete[] data;
      data = nullptr;
      std::cout << "read file failed.\n";
      return FAILED;
    }

    int ret = RunSession(data, inputWeightShape, paths, compressParameters);
    delete[] data;
    data = nullptr;

    if (ret != SUCCESS){
      std::cout << "run session failed.\n";
      return FAILED;
    }
  } catch (const std::exception& e) {
    delete[] data;
    data = nullptr;
    std::cout << "read file or run session failed.\n";
    return FAILED;
  }
  return SUCCESS;
}
