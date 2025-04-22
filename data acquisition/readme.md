# Notice
In order to call the OpenWeather API for your location data you will need the following:
- A Open weather account
- Your API key
## How to get an API key
1. Sign up at https://home.openweathermap.org/users/sign_up
2. Login to your account
3. Navigate to API keys
4. Select or Generate a new API key
## calling the API
The api is structured like this:
```
https://api.openweathermap.org/data/2.5/{service}?{parameters}"
```
- Service is the API endpoint to call
- parameters are query parameters used to call the APi

The node red flows use the current weater API
```
https://api.openweathermap.org/data/2.5/weather?lat={your_lat}&lon={your_lon}&appid={your_api_key}&units=metric"
```
To use the flow
- Replace `your_lat` and `your_lon` with latitude and logitude of the location you wish to optain weather data for
- replace `your_api_key` with your OpenWeather API key

# node-RED flows
- flows_api is a flow for collecting weather data with just the OpenWeather API
- flows_sensor is a flow for collecting weather data in conjunction with the API
- flows_complete is a flow that collects weather data with sensor and performs data integration to the cleaned table automatically
