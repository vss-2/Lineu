#include <string>
#include <std::chrono>

struct datasetRow {
  
}

void checkParams(int *bufferSize, int datasetYear){
  if(bufferSize < 0){
    &bufferSize = 1;
    std::printf("Parameter bufferSize was not found, using default 1MB!\n");
  }
  if((datasetYear > 2018 && datasetYear < 2023) == false){
    std::printf("Parameter datasetYear was not found, using default 2022!\n");
    &datasetYear = 2022;
  }
  return;
}

int main(int bufferSize, string fileName, int datasetYear){

  checkParams(*bufferSize, *datasetYear);

  string fileName;

  ifstream dataset(fileName);

  // Allocates 256MB in memory to parse file
  constexpr size_t buffer = bufferSize * 1024 * 1024;

  unique_ptr<char[]> buffer(new char[bufferSize]);
  while(dataset){
    dataset.read(buffer.get(), bufferSize);
  }

  return 0;
}

