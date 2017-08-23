/************************************************************************

            BLOCKCHAIN AGRI USECASE (MULTI CHAIN)

*************************************************************************/

var farm_warehouse_shop_hexblob = '';
var warehouse_shop_hexblob = '';

// Initialize Pubnub

pubnub = new PubNub({
    publishKey : 'pub-c-abde89c6-da51-4c04-8c2b-9c3984e1182d',
    subscribeKey : 'sub-c-d17a927c-e171-11e6-802a-02ee2ddab7fe'
})
   
/***************************************************************************************
    Function      : publishMessage
    Channel       : farmland , warehouse and retailstore
    Parameters    : channel name , message to be sent
    Description   : Publishes message to pubnub channel 
****************************************************************************************/

    function publishMessage(channel,msg) {
        console.log(channel,msg)
        pubnub.publish(
        {
            message: msg,
            channel: channel,
            storeInHistory: true //override default storage options
        });
    } 

/***************************************************************************************
    Function      : pubnub Listener 
    Channel       : UI
    Description   : Fetches the received message and forwards to data operation function
****************************************************************************************/ 
    pubnub.addListener({
        message: function(m) {
            console.log("Received Message!!", m.message);
            messageOnReceive(m.message)
        }
    })      

/***************************************************************************************
    Function      : pubnub subscribe
    Channel       : UI
    Description   : Subscribes to pubnub channel to receive blockchain node data
****************************************************************************************/       
    pubnub.subscribe({
        channels: ['UI'] 
    });

/***************************************************************************************
    Function      : dynTable
    Parameters    : Table data , Table name
    Description   : Dynamically generate table with passed data (list of data)
****************************************************************************************/ 
    function dynTable(data,tname){
        if(tname == "farmland"){
            var datatable = $('#FarmLand-Table');
        }else if(tname == "warehouse"){
            var datatable = $('#Warehouse-Table');
        }else if(tname == "retailstore"){
            var datatable = $('#Retailshop-Table');
        }
        var tdata = data;
        var tbody = $('<tbody>');
        var thead = $('<thead>');
        var th = $('<tr>'+
                        '<th>Name</th>'+
                        '<th>Quantity</th>'+
                        '<th>Units</th>'+
                        '<th>Owner</th>'+
                    '</tr>');
        thead.append(th);
        datatable.append(thead);
        // list of table data
        tdata.forEach(function(user) {
            console.log(user)
            var tr = $('<tr>');
            ['assetname', 'assetquantity', 'assetmetrics','assetowner'].forEach(function(attr) {
                tr.append('<td>' + user[attr] + '</td>');
            });
            tbody.append(tr);
        });
        datatable.append(tbody);
    }

/***************************************************************************************
    Function      : UpdateTable
    Parameters    : Table name , Table data 
    Description   : Dynamically generate table with passed data(instant individual data)
****************************************************************************************/ 
    function UpdateTable(tname,data){
        if(tname == "farmland"){
            var datatable = $('#FarmLand-Table');
            console.log(datatable)
        }else if(tname == "warehouse"){
            var datatable = $('#Warehouse-Table');
        }else if(tname == "retailstore"){
            var datatable = $('#Retailshop-Table');
        }
        var tdata = data;
        var tbody = $('<tbody>');
        var thead = $('<thead>');
        var th = $('<tr>'+
                        '<th>Name</th>'+
                        '<th>Quantity</th>'+
                        '<th>Units</th>'+
                        '<th>Owner</th>'+
                    '</tr>');
        thead.append(th);
        datatable.append(thead);
        
        var tr = $('<tr>');
        // received table values
            ['assetname', 'assetquantity', 'assetmetrics','assetowner'].forEach(function(attr) {
                tr.append('<td>' + tdata[attr] + '</td>');
            });
            tbody.append(tr);
        datatable.append(tbody);
    }

/***************************************************************************************
    Function      : ExchangeTable
    Parameters    : Table name ,Table data_offer , Table data_ask
    Description   : Dynamically generate exchangetable with passed data 
****************************************************************************************/ 
    function ExchangeTable(tname,data_offer,data_ask){
        if(tname == "farmland"){
            var datatable = $('#Farm-Warehouse-Table');
        }else if(tname == "warehouse"){
            var datatable = $('#Warehouse-Retailshop-Table');
        }
        var tbody = $('<tbody>');
        var thead = $('<thead>');
        var th = $('<tr>'+
                        '<th>Offer-Assetname</th>'+
                        '<th>Offer-Assetquantity</th>'+
                        '<th>Ask-Assetname</th>'+
                        '<th>Ask-Assetquantity</th>'+
                    '</tr>');
        thead.append(th);
        datatable.append(thead);
        
        var tr = $('<tr>');
        // data_offer
            ['name', 'qty'].forEach(function(attr) {
                tr.append('<td>' + data_offer[attr] + '</td>');
            });
        // data_ask
            ['name', 'qty'].forEach(function(attr) {
                tr.append('<td>' + data_ask[attr] + '</td>');
            });
            tbody.append(tr);
        datatable.append(tbody);
    }

/***************************************************************************************
    Function      : messageOnReceive
    Parameters    : message received from blockchain nodes
    Description   : Diplays the visual indication on receiving message from blockchain nodes
****************************************************************************************/ 
    function messageOnReceive(m){

    // Decode Exchange between farmland and warehouse

        if(m.messagecode == "decodeexchange" && m.messagetype == "resp" && m.node == "warehouse"){
            if(m.message.exchange_details != false && m.message.exchange_addedtochain != false){
                $('#arrow1').css({fill:"#7CFC00"});
                $('#Farm-Warehouse-Table').empty();
                var data_offer = m.message.exchange_details.offer.assets[0]
                var data_ask = m.message.exchange_details.ask.assets[0]
                ExchangeTable("farmland",data_offer,data_ask)

            }else
            {
                $('input:radio[name=createExchange]:nth(1)').attr('checked',false);
                alert("error")
            }
        }

    // Decode Exchange between warehouse and retailstore

        else if(m.messagecode == "decodeexchange" && m.messagetype == "resp" && m.node == "retailstore"){
            if(m.message.exchange_details != false && m.message.exchange_addedtochain != false){
                $('#arrow2').css({fill:"#7CFC00"});
                $('#Warehouse-Retailshop-Table').empty();
                var data_offer = m.message.exchange_details.offer.assets[0]
                var data_ask = m.message.exchange_details.ask.assets[0]
                ExchangeTable("warehouse",data_offer,data_ask)

            }else
            {
                $('input:radio[name=createExchange]:nth(3)').attr('checked',false);
                alert("error")
            }
        }

    // Create Exchange between farmland and warehouse

        else if(m.messagecode == "createexchange" && m.messagetype == "resp" && m.node == "farmland"){
            // create exchange top level error handling
            if(m.message == ""){
                console.log(m.message.error)
                $('input:radio[name=createExchange]:nth(0)').attr('checked',false);
                alert(m.message.error)
            }
            // create exchange API level error handling
            else if(m.message.hexblob == ""){
                $('input:radio[name=createExchange]:nth(0)').attr('checked',false);
                alert("API error")
            }else{
                console.log("reached")
                farm_warehouse_shop_hexblob = m.message.hexblob;
                $('#arrow1').css({fill:"#FF4500"});
            }
        }

    // Create Exchange between warehouse and retailstore

        else if(m.messagecode == "createexchange" && m.messagetype == "resp" && m.node == "warehouse"){
            // create exchange top level error handling
            if(m.message == ""){
                console.log(m.message.error)
                $('input:radio[name=createExchange]:nth(2)').attr('checked',false);
                alert(m.message.error)
            }
            // create exchange API level error handling
            else if(m.message.hexblob == ""){
                $('input:radio[name=createExchange]:nth(2)').attr('checked',false);
                alert("API error")
            }else{
                farm_warehouse_shop_hexblob = m.message.hexblob;
                $('#arrow2').css({fill:"#FF4500"});
            }
        }

    // Issueing farmland asset

        else if(m.messagecode == "issueasset" && m.messagetype == "resp" && m.node == "farmland"){
            if(m.message["op_return"]["error"] != undefined || m.message["op_return"] == "error" || m.message["op_return"] == false){
                $('input:radio[name=IssueAsset]:nth(0)').attr('checked',false);
                alert("error")
            }else
            {
                $('#step_1_circle').css({fill:"#7CFC00"});
                var data = m.message.assetdescription
                UpdateTable("farmland",data)
                
            }
        }
    // // Issueing warehouse asset

        else if(m.messagecode == "issueasset" && m.messagetype == "resp" && m.node == "warehouse"){
            if(m.message["op_return"]["error"] != undefined || m.message["op_return"] == "error" || m.message["op_return"] == false){
                $('input:radio[name=IssueAsset]:nth(1)').attr('checked',false);
                alert("error")
            }else
            {
                $('#step_2_circle').css({fill:"#7CFC00"});
                var data = m.message.assetdescription
                UpdateTable("warehouse",data)
                
            }
        }

    // Issueing retailstore asset

        else if(m.messagecode == "issueasset" && m.messagetype == "resp" && m.node == "retailstore"){
            if(m.message["op_return"]["error"] != undefined || m.message["op_return"] == "error" || m.message["op_return"] == false){
                $('input:radio[name=IssueAsset]:nth(2)').attr('checked',false);
                alert("error")
            }else
            {
                $('#step_3_circle').css({fill:"#7CFC00"});
                var data = m.message.assetdescription
                UpdateTable("retailstore",data)
                
            }
        }

    // Updating farmland asset balances

        else if(m.messagecode == "updateassetbalance" && m.messagetype == "resp" && m.node == "farmland"){
            if(m.message["op_return"] == "error" || m.message["op_return"] == false){
                alert("error")
            }else
            {   
                $('#FarmLand-Table').empty();
                var table = "farmland"
                var data = m.message.op_return
                dynTable(data,table)
            }
        }

    // Updating warehouse asset balances

        else if(m.messagecode == "updateassetbalance" && m.messagetype == "resp" && m.node == "warehouse"){
            if(m.message["op_return"] == "error" || m.message["op_return"] == false){
                alert("error")
            }else
            {
                $('#Warehouse-Table').empty();
                var table = "warehouse"
                var data = m.message.op_return
                dynTable(data,table)
            }
        }

    // Updating retailstore asset balances

        else if(m.messagecode == "updateassetbalance" && m.messagetype == "resp" && m.node == "retailstore"){
            if(m.message["op_return"] == "error" || m.message["op_return"] == false){
                alert("error")
            }else
            {
                $('#Retailshop-Table').empty();
                var table = "retailstore"
                var data = m.message.op_return
                dynTable(data,table)
            }
        }
    }


$(document).ready(function(){ 

// Onclick "start process" button sends "convertasset" message to warehouse node

    $("#startProcess").click(function(){
        var publishMsg = { "messagecode":"convertasset","messagetype":"req"}
        var channel = "warehouse"
        publishMessage(channel,publishMsg)
        
        var publishMsg = { "messagecode":"updateassetbalance","messagetype":"req"}
        var channel = "warehouse"
        setTimeout(function(){
            publishMessage(channel,publishMsg)
        },3000);
    });

// Onclick "get updated bal" button sends update request to all three nodes

    $("#getUpdatebal").click(function(){
        var publishMsg = { "messagecode":"updateassetbalance","messagetype":"req"}
        var channel = "farmland"
        publishMessage(channel,publishMsg)

        setTimeout(function(){
            var channel = "warehouse"
            publishMessage(channel,publishMsg)
        },2000);
                
        setTimeout(function(){
            var channel = "retailstore"
            publishMessage(channel,publishMsg)
        },2000);
    });

// RadioButton select - Issue Asset

    $('#IssueAsset-farm').click(function(){
        $('input:radio[name=IssueAsset]:nth(0)').attr('checked',true);
        var publishMsg = { "messagecode":"issueasset","messagetype":"req"}
        var channel = "farmland"
        publishMessage(channel,publishMsg)
    })
    $('#IssueAsset-warehouse').click(function(){
        $('input:radio[name=IssueAsset]:nth(1)').attr('checked',true);
        var publishMsg = { "messagecode":"issueasset","messagetype":"req"}
        var channel = "warehouse"
        publishMessage(channel,publishMsg)
    })
    $('#IssueAsset-retailshop').click(function(){
        $('input:radio[name=IssueAsset]:nth(2)').attr('checked',true);
        var publishMsg = { "messagecode":"issueasset","messagetype":"req"}
        var channel = "retailstore"
        publishMessage(channel,publishMsg)
    })

// RadioButton select - CreateExchange and Decode Exc Asset

    $('#createExchange-farm-warehouse').click(function(){
        $('input:radio[name=createExchange]:nth(0)').attr('checked',true);
        var publishMsg =  {"messagetype":"req","messagecode":"createexchange"}
        var channel = "farmland"
        publishMessage(channel,publishMsg)
    })
    $('#Decode-Exchange-farm-warehouse').click(function(){
        $('input:radio[name=createExchange]:nth(1)').attr('checked',true);
        var publishMsg =  {"messagetype":"req","messagecode":"decodeexchange","hexblob":farm_warehouse_shop_hexblob}
        var channel = "warehouse"
        publishMessage(channel,publishMsg)
    })
    $('#createExchange-warehouse-shop').click(function(){
        $('input:radio[name=createExchange]:nth(2)').attr('checked',true);
        $('#arrow2').css({fill:"#FF4500"});
        var publishMsg =  {"messagetype":"req","messagecode":"createexchange"}
        var channel = "warehouse"
        publishMessage(channel,publishMsg)
    })
    $('#Decode-Exchange-warehouse-shop').click(function(){
        $('input:radio[name=createExchange]:nth(3)').attr('checked',true);
        var publishMsg =  {"messagetype":"req","messagecode":"decodeexchange","hexblob":farm_warehouse_shop_hexblob}
        var channel = "retailstore"
        publishMessage(channel,publishMsg)
    })

});