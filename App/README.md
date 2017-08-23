# Blockchain in AGRI

## To Run the demo

### Step 1:
Open the UI file in a browser

        App/blockchainui.html

### Step 2: IssueAsset procedure

    1.Click on the radio button under IssueAsset heading to issue FARMLAND asset
    2.Click on the radio button under IssueAsset heading to issue WAREHOUSE asset
    3.Click on the radio button under IssueAsset heading to issue RETAILSTORE asset

On successful asset creation , farm / warehouse / retailstore icon turns to GREEN 

### Step 3: Create Exchange procedure (FARMLAND-WAREHOUSE)

    Click on the radio button under Create Exchange heading to issue FARMLAND-WAREHOUSE asset
    
On successful Exchange creation , FARMLAND-WAREHOUSE / WAREHOUSE-RETAILSTORE arrow icon turns to ORANGE 

### Step 4: Decode Exchange procedure (FARMLAND-WAREHOUSE)

    Click on the radio button under Decode Exchange heading to issue FARMLAND-WAREHOUSE asset
    
On successful Decode Exchange creation , FARMLAND-WAREHOUSE / WAREHOUSE-RETAILSTORE arrow icon turns to GREEN 

### Step 5: Getting updated asset balances
    
    Click on the "Get Updated Bal" button under Asset Processing heading to get the upated balances of each asset
    
### Step 6: Asset Processing

    Click on the AssetProcess button under Asset Processing heading to process 
    the raw farmland asset to processed warehouse asset.

### Step 7: Create Exchange procedure (WAREHOUSE-RETAILSTORE)

    Click on the radio button under Create Exchange heading to issue WAREHOUSE-RETAILSTORE asset
    
On successful Exchange creation , WAREHOUSE-RETAILSTORE arrow icon turns to ORANGE 

### Step 8: Decode Exchange procedure (WAREHOUSE-RETAILSTORE)

    Click on the radio button under Decode Exchange heading to issue WAREHOUSE-RETAILSTORE asset
    
On successful Decode Exchange creation , WAREHOUSE-RETAILSTORE arrow icon turns to GREEN

### Step 9: Getting updated asset balances
    
    Click on the "Get Updated Bal" button under Asset Processing heading to get the upated balances of each asset
    
### Step 10: Delete chain
To delete the chain , execute [this](https://github.com/AravindNico/blockchain_agri_usecase/blob/master/deletechain.sh) file in the root directory of this repository

        sh deletechain.sh
    
