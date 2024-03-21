# Stock Analysis

In this project it will be possible to observe the behavior of the stock market with different options to add statistical indicators to determine this behavior taking as reference the opening and closing values, highest and lowest value reached, etc.

## To dockerize this file and be able to view the application, you must execute the following lines of code:

docker build -t finance_app .
docker run -h localhost -p 5002:5000 -d --name finance_app finance_app