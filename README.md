# Blockchain-Agri-Usecase-using-Multichain

### Step 1 : 
Download the [Docker image](https://drive.google.com/file/d/0B_tUIxE370NmQVdsR2hnbU5rNlk/view)

### Step 1.1 : 
Copy to the home folder and load the docker by running the following command

		sudo docker load --input multichaindocker
		
![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d29.png)

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d30.png)		

### Step 1.2 : 
Run the following command to check installed image.
		
		sudo docker images

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d31.png)		

## Note : This docker image has the following things installed.
		
	pip

	wget

	multichain [link](http://www.multichain.com/download-install/)

	Savoir [link](https://github.com/DXMarkets/Savoir)

	Pubnub==3.8.3 [link](https://www.pubnub.com/docs/python/pubnub-python-sdk)

	logging 

	git

### Step 2 : 
Open three terminals and run the docker image in three terminals.

## Note : Decide the terminals with the names 
	   
	   example :
	   			container 1 - farmland 
	   			container 2 - warehouse
	   			container 3 - retailstore

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d1.png)

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d2.png)

### Step 3 : 
Run <strong>cd</strong> in each container.

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d3.png)

### Step 4 : 
Clone the [blockchain_agri_usecase repository](https://github.com/AravindNico/blockchain_agri_usecase.git) in three containers.

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d4.png)

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d5.png)

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d6.png)

### Step 5 : 
Choose the farmland contianer as the admin by starting the chain in the farmland container

### Step 5.1 : 
Run the command "multichain-util create chain1" in the farmland container.

	multichain-util create chain1

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d8.png)
 
![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d9.png)

### Step 5.2 : 
Run the command "multichaind chain1 -daemon"

	multichaind chain1 -daemon

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d10.png)

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d11.png)

### Step 6 : 
Connect to the chain from the other(warehouse,retailstore) containers.

### Step 6.1 : 
Copy the command that given when you started the chain in farmland.

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d12.png)

### Step 6.2 : 
Run that command in other contatiners.

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d13.png)

### Step 7 : 
Now we have to give permissions for the other containers.

### Step 7.1 : 
Copy the line that you got in the above operation.

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d14.png)

### Step 7.2 : 
Paste it in the admin(farmland) container and add two more permissions 
		 
		 1) issue 
		 2) mine

and run the command		


![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d15.png)

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d16.png)

### Step 7.3 : 
Please follow the same procedure to give permissions for the retailstore container.


![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d16.png)


![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d17.png)


![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d19.png)

Now permissions are granted for the warehouse and retailstore containers.


### Step 8 : 
Now we have to start the chain from the warehouse and retailstore containers.

	multichaind chain1 -daemon

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d20.png)

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d21.png)

### Step 9 : 
Next have to give permission for the burnaddress of the chain.

### Step 9.1 : 
Run the following command to get the info about the chain.
	
		multichain-cli chain1 getinfo

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d22.png)

### Step 9.2 : 
Copy the burnaddress

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d23.png)

### Step 9.3 : 
Grant receive permission to the burn address by running following command.

	multichain-cli chain1 grant <copied burnaddress> receive.

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d24.png)

### Step 10 : 
Now goto the repository root folder and run the following [get.sh](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/get.sh) to get the values for rpcuser,rpcport,rpcpassword

## Note : Run this program in three containers and save those values.
	Run the following command 

		sh get.sh

		1.rpcuser
		2.rpcport
		3.rpcpassword


![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d26.png)



### Step 11 : 
Now goto the respective folders in the container.

		container 1 - Farmland folder
		container 2 - Warehouse folder
		container 3 - Retailstore folder

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d25.png)

### Step 11.1 : 
Open the config.ini program in each container and paste those copied values from the step 10, and save.

### Step 12 : 
Now the run the programs in three containers.

	container1 - python farmland.py
	container2 - python warehouse.py
	container3 - python retailstore.py

![alt-tag](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/screenshots/d28.png)


