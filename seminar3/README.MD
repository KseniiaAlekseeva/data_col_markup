https://stackoverflow.com/questions/65357744/how-to-install-mongodb-on-apple-m1-chip

Article on how to install mongodb on apple m1 using homebrew

Install homebrew from https://brew.sh/
Install xcode command line using
```commandline
xcode-select --install
```
Now to install mongodb use

```commandline
brew tap mongodb/brew
brew install mongodb-community@7.0
```

To check if mongodb has been installed use
```commandline
mongod --version
```
to start mongoDB as macOS service use
```commandline
brew services start mongodb-community@7.0
```

and to stop mongoDB to run as a background service use

```commandline
brew services stop mongodb-community@7.0
```

Or, if you don't want/need a background service you can just run:
```commandline
mongod --config /opt/homebrew/etc/mongod.conf
```

To run mongodb commands, open a new table and run mongo
To check your databases run 
```commandline
show dbs
```
