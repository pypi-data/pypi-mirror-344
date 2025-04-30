class HP:
    codes = [
        '''
unsigned long long factorial(int n) {
    unsigned long long result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    int n;
    printf("Enter a number to compute its factorial: ");
    scanf("%d", &n);

    clock_t start = clock();
    unsigned long long result = factorial(n);
    clock_t end = clock();

    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("Factorial of %d is %llu\n", n, result);
    printf("Time taken (Serial): %f seconds\n", time_taken);

    return 0;
    
}
        ''',
        '''
#include <stdio.h>
#include <omp.h>

#define FUNC(x) ((x)*(x))  // f(x) = x^2

double trapezoidal_integral(double a, double b, int n, int num_threads) {
    double h = (b - a) / n;
    double integral = 0.0;

    #pragma omp parallel num_threads(num_threads)
    {
        int thread_id = omp_get_thread_num();
        int thread_count = omp_get_num_threads();
        int local_n = n / thread_count;

        double local_a = a + thread_id * local_n * h;
        double local_b = local_a + local_n * h;
        double local_sum = (FUNC(local_a) + FUNC(local_b)) / 2.0;

        for (int i = 1; i < local_n; i++) {
            double x = local_a + i * h;
            local_sum += FUNC(x);
        }

        local_sum *= h;

        #pragma omp atomic
        integral += local_sum;

        printf("Thread %d handling interval [%.5f, %.5f]\n", thread_id, local_a, local_b);
    }

    return integral;
}
        ''',
        '''
#include<iostream>
#include<vector>
#include<mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int world_size, world_rank;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    std::vector<int> array = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int array_size = array.size();

    if (world_size != 3) {
        if (world_rank == 0) {
            std::cerr << "This program requires exactly 3 processes." << std::endl;
        }
        MPI_Finalize();
        return 1;
    }

    int split_size = array_size / 2;
    std::vector<int> sub_array(split_size);

    double start_time = MPI_Wtime();

    if (world_rank == 0) {
        // Send first half to process 1
        MPI_Send(array.data(), split_size, MPI_INT, 1, 0, MPI_COMM_WORLD);
        // Send second half to process 2
        MPI_Send(array.data() + split_size, split_size, MPI_INT, 2, 0, MPI_COMM_WORLD);
    } else {
        // Receive subarray from process 0
        MPI_Recv(sub_array.data(), split_size, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        // Compute local sum
        int local_sum = 0;
        for (int i = 0; i < split_size; ++i) {
            local_sum += sub_array[i];
        }

        // Send result back to process 0
        MPI_Send(&local_sum, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }

    if (world_rank == 0) {
        int sum1 = 0, sum2 = 0;
        MPI_Recv(&sum1, 1, MPI_INT, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(&sum2, 1, MPI_INT, 2, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        int final_sum = sum1 + sum2;

        double end_time = MPI_Wtime();
        double processing_time = end_time - start_time;

        std::cout << "Final Sum: " << final_sum << std::endl;
        std::cout << "Processing Time: " << processing_time << " seconds" << std::endl;
    }

    MPI_Finalize();
    return 0;
}
        ''',
        '''
#include <mpi.h>
#include <iostream>
#include <vector>

#define ARRAY_SIZE 500

void stage_1(double& num) { num = 4; }
void stage_2(double& num) { num = 5; }
void stage_3(double& num) { num += 3; }
void stage_4(double& num) { num = 7; }

int main(int argc, char* argv[]) {
    int rank, size;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size != 5) {
        if (rank == 0) {
            std::cerr << "Error: This program requires exactly 5 processes." << std::endl;
        }
        MPI_Finalize();
        return 1;
    }

    std::vector<double> input(ARRAY_SIZE);

    if (rank == 0) {
        // Initialize input array
        for (int i = 0; i < ARRAY_SIZE; i++) {
            input[i] = static_cast<double>(i + 14);  // Example input values
        }

        // Send values to stage 1
        for (int i = 0; i < ARRAY_SIZE; i++) {
            double num = input[i];
            MPI_Send(&num, 1, MPI_DOUBLE, 1, 0, MPI_COMM_WORLD);
        }
    }

    else if (rank == 1) {
        for (int i = 0; i < ARRAY_SIZE; i++) {
            double num;
            MPI_Recv(&num, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            stage_1(num);
            MPI_Send(&num, 1, MPI_DOUBLE, 2, 0, MPI_COMM_WORLD);
        }
    }

    else if (rank == 2) {
        for (int i = 0; i < ARRAY_SIZE; i++) {
            double num;
            MPI_Recv(&num, 1, MPI_DOUBLE, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            stage_2(num);
            MPI_Send(&num, 1, MPI_DOUBLE, 3, 0, MPI_COMM_WORLD);
        }
    }

    else if (rank == 3) {
        for (int i = 0; i < ARRAY_SIZE; i++) {
            double num;
            MPI_Recv(&num, 1, MPI_DOUBLE, 2, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            stage_3(num);
            MPI_Send(&num, 1, MPI_DOUBLE, 4, 0, MPI_COMM_WORLD);
        }
    }

    else if (rank == 4) {
        for (int i = 0; i < ARRAY_SIZE; i++) {
            double num;
            MPI_Recv(&num, 1, MPI_DOUBLE, 3, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            stage_4(num);
            std::cout << "Output [" << i << "]: " << num << std::endl;
        }
    }

    MPI_Finalize();
    return 0;
}
        ''',
        '''
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

void bubble_sort(int arr[], int n) {
    int i, j, temp;
    for (i = 0; i < n - 1; i++) {
        for (j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int main(int argc, char* argv[]) {
    int rank, size, n = 10;
    int arr[10] = {34, 7, 23, 32, 5, 62, 32, 78, 56, 99};

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Divide array into local portions for each process
    int local_n = n / size;
    int* local_arr = (int*)malloc(local_n * sizeof(int));

    double start_time = MPI_Wtime();
    
    // Scatter data to all processes
    MPI_Scatter(arr, local_n, MPI_INT, local_arr, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    // Perform local bubble sort
    double local_start_time = MPI_Wtime();
    bubble_sort(local_arr, local_n);
    double local_end_time = MPI_Wtime();

    // Gather sorted local arrays back to root process
    MPI_Gather(local_arr, local_n, MPI_INT, arr, local_n, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        // Perform global bubble sort on the gathered array
        double global_start_time = MPI_Wtime();
        bubble_sort(arr, n);
        double global_end_time = MPI_Wtime();

        // Output sorted array
        printf("Sorted array: ");
        for (int i = 0; i < n; i++) {
            printf("%d ", arr[i]);
        }
        printf("\n");

        // Print timing results
        printf("Local sort time: %f seconds\n", local_end_time - local_start_time);
        printf("Global sort time: %f seconds\n", global_end_time - global_start_time);
    }

    // Output total execution time
    double end_time = MPI_Wtime();
    if (rank == 0) {
        printf("Total execution time: %f seconds\n", end_time - start_time);
    }

    // Free allocated memory
    free(local_arr);

    MPI_Finalize();
    return 0;
}
        ''',
        '''
Nahi hai
        ''',
        '''
#include <iostream>
#include <cuda_runtime.h>

#define N 1024

// CUDA kernel for matrix multiplication
_global_ void matrixMultiply(float* A, float* B, float* C, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < n && col < n) {
        float sum = 0.0f;
        for (int k = 0; k < n; k++) {
            sum += A[row * n + k] * B[k * n + col];
        }
        C[row * n + col] = sum;
    }
}

int main() {
    int size = N * N * sizeof(float);
    float *h_A, *h_B, *h_C, *d_A, *d_B, *d_C;

    // Allocate host memory
    h_A = (float*)malloc(size);
    h_B = (float*)malloc(size);
    h_C = (float*)malloc(size);

    // Allocate device memory
    cudaMalloc(&d_A, size);
    cudaMalloc(&d_B, size);
    cudaMalloc(&d_C, size);

    // Initialize matrices A and B with some values (e.g., 1.0f for simplicity)
    for (int i = 0; i < N * N; i++) {
        h_A[i] = 1.0f;  // Example: set all elements to 1.0f
        h_B[i] = 1.0f;  // Example: set all elements to 1.0f
    }

    // Copy matrices A and B from host to device
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);

    // Set up the execution configuration (grid and block dimensions)
    int threadsPerBlock = 16;
    dim3 blockDim(threadsPerBlock, threadsPerBlock); // 16x16 threads per block
    dim3 gridDim((N + threadsPerBlock - 1) / threadsPerBlock, (N + threadsPerBlock - 1) / threadsPerBlock); // Grid size

    // Launch kernel
    matrixMultiply<<<gridDim, blockDim>>>(d_A, d_B, d_C, N);

    // Check for errors in kernel launch
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        std::cerr << "CUDA error: " << cudaGetErrorString(err) << std::endl;
        return -1;
    }

    // Copy the result matrix C from device to host
    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);

    // Display a sample result (the first element in C)
    std::cout << "Sample Output: " << h_C[0] << std::endl;

    // Free allocated memory
    free(h_A);
    free(h_B);
    free(h_C);
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);

    return 0;
}
        ''',
    ]

    @staticmethod
    def text(index):
        """Fetch a specific code based on the index."""
        try:
            return HP.codes[index - 1]
        except IndexError:
            return f"Invalid code index. Please choose a number between 1 and {len(HP.codes)}."
