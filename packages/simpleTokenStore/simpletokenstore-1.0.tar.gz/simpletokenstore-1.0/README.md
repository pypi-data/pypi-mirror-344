### SimpleTokenStore 
The easiest way to manage session tokens.   
Are you tired of retrieving session tokens when developing your API interfaces? Do you end up retrieving a new one every time you debug your code? Does your AWS lambda function need to store an api key temporarily? Look no further!

### Use Cases:   
If you're developing locally and working with api tokens, or using a serverless function like an AWS lambda, you probably want to store session tokens. This library allows you to use them without any overhead. 
You don't have to worry about token expiry, or storing them in a local file and reading it. 
### Setup  
There are only 2 parts of this libray to interface with    
### 1. Instantiate the token store.     
You have a function used to retrieve a new session token, instanitate the token store and pass this in as 'get_new_token_function', for example, if 'new_session' is my function to get a new session token I would write:
```
resource = SimpleTokenStore(get_new_token=new_session)
```
(note, it's not new_session(), which would return the result of that call, it's the function itself, a **callable**).
### 2. Getting a new token
Call 'collect_token' to retrieve a token, this handles retrieving cached tokens for you. Like this 
```
session_token = resource.collect_token()
```
Now every time you call __resource.collect_token()__ it will get a token for you, using a cached token if available, and getting a new one when required. 
## Configuration
To make things super-easy, there are 2 assumptions made if you don't change any settings when using the library. 
1. tokens are valid for 30 minutes   
2. you only want to store one token at a time  

If either of these are not true, here's how you change it.
### Changing token lifetime
Tokens are stored alongside an expiry time, if you want a custom time just add the `expires_in_minutes` argument to the instanitation. For example 
```
resource = SimpleTokenStore(get_new_token=new_session, expires_in_minutes=60)
```
would make any stored token valid for 60 minutes from its first saving. Any call to resource.collect_token() after this call for 60 minutes will use the stored token rather than the using the new_session call. 
### Storing multiple tokens
If you're storing more than one session token, just pass in a value when calling 'collect_token', future calls will store and retrieve a session token from this same key.   
For example if I want to store a 'beta' key I would call 
```
resource.collect_token('beta')
```
and this would store the token separately from the calls to 
```
resource.collect_token('prod')
```
If I have different methods for retrieving tokens I would create different instances of the SimpleTokenStore, and use different calls to collect_token (passing in different strings) to make sure their stored session tokens don't overwrite each other. 