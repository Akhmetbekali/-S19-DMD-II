# -S19-DMD-II

## Cassandra Project for Databases and Data Modeling Class 2019

In the project we have created database schema that best suits apache cassandra.

### [Documentation](DOCUMENTATION.md)

To run our project on your PC

* First you have to install cassandra from their site
```cassandra.apache.org```

* Then (if you are on windows) add it to environmental variables.

* Open command line and type 
```cassandra```

* Open ```/usr/local/etc/cassandra/cassandra.yaml``` 
    * Change ```authenticator: AllowAllAuthenticator``` to ```authenticator: PasswordAuthenticator```
    * Change ```authorizer: AllowAllAuthorizer``` to ```authorizer: CassandraAuthorizer```

* Now you are running cassandra server on 127.0.0.1:PORT

* Install python and pip

* Now you have to add packages for the project to run correctly
note order of download is not important.

``` pip3 install -r requirements.txt ```

* Now make your working directory is ```-S19-DMD-II``` and run the following script

```python CassandraDriver.py ```
- this will create the tables and index these tables.

* To populate the tables with -somehow- random data run
```python Randomizer.py ```
