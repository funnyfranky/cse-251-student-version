/************************************
Course: cse 251
File: team1.java
Week: week 11 - team activity 1

Instructions:

- Main contains an array of 1,000 random values.  You will be creating
  threads to process this array.  If you find a prime number, display
  it to the console.

- DON'T copy/slice the array in main() for each thread.

Part 1:
- Create a class that is a sub-class of Thread.
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 2:
- Create a class on an interface or Runnable
- create 4 threads based on this class you created.
- Divide the array among the threads.

Part 3:
- Modify part1 or part 2 to handle any size array and any number
  of threads.

************************************/
import java.util.Random; 
import java.lang.Math; 

public class team1 {

  static boolean isPrime(long n) 
  { 
      // Corner cases 
      if (n <= 1) return false; 
      if (n <= 3) return true; 
    
      // This is checked so that we can skip  
      // middle five numbers in below loop 
      if (n % 2 == 0 || n % 3 == 0) return false; 
    
      for (long i = 5; i * i <= n; i = i + 6) 
        if (n % i == 0 || n % (i + 2) == 0) 
          return false; 
    
      return true; 
  }

  public static void main(String[] args) {
    System.out.println("Hello world!");

    // create instance of Random class 
    Random rand = new Random(); 
    int threadCount = 4;
    int count = 10000;
    long[] array = new long[count];
    for (int i = 0; i < count; i++)
    {
      array[i] = Math.abs(rand.nextInt());
    }

    Thread[] threads = new Thread[threadCount];
    // for i in range(0,threadCount) {};

    threads[0] = new Thread(new Runnable() { // TODO Change 0 to i for loop
      public void run() {
        for (int i = 0; i < count/threadCount; i++) 
        {
          if (isPrime(array[i]))
          {
            System.out.println("Thread 1: " + array[i]);
          }
        }
      }
    });
    threads[0].start();

    // // TODO - this is just sample code. you can remove it.
  //   for (int i = 0; i < count; i++) 
  //   {
  //     if (isPrime(array[i]))
  //     {
  //       System.out.println(array[i]);
  //     }
  //   }
  }
}