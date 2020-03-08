FORMAT: 1A


# Car installment calculator[]

## Paymentplan Collection[/{handle}]

Collection of all paymentplans for a handle


+ Parameters

    + handle(string, unique) - A handle for grouping sets of paymentplans(handle)

    
### List of all paymentplans that are associated with the handle [GET]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
+ Response 200 (application/vnd.mason+json)

    + Body
        {
            {
            "totalprice": 1400.0,
            "model": "Jetta",
            "provider": "JussinAutopiste"
            "manufacturer": "Volkswagen",
            "key": "jussinautopistejetta",
            "open": True
            }
        }
    
### Modify handle[PUT]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
    + Body
        
        {
            {
            "name" : "Pyrynhandle",
            "type" : "Individual"
            }
        
        }
+ Response 200 (application/vnd.mason+json)

### Delete handle[DELETE]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
+ Response 200 (application/vnd.mason+json)

        
### Posts a new Paymentplan[POST]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
    + Body
    
        {
        "price": 10238.0,
        "interestrate": 5.0,
        "months": 6,
        "provider": "PyrynSuperAutot"
        "payers": 1,
        "open": True,
        "carmodel": "toyotacorolla"
        }
        
+ Response 200 (application/vnd.mason+json)
 
 
## Open Paymentplan Collection[/{handle}/open]

Collection of paymentplans that haven't been paid yet

+ Parameters

    + handle(string, unique) - A handle for grouping sets of paymentplans(handle)
    

### Lists all open paymentplans under the handle [GET]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
+ Response 200 (application/vnd.mason+json)

    + Body
        {
            {
            "totalprice": 1400.0,
            "model": "Jetta",
            "manufacturer": "Volkswagen",
            "key": "volkswagenjetta",
            "open": True
            }
        }

## Model Collection[/{handle}/models]

Collection of all the models that are associated with the handle

### Gives all Models associated with the handle[GET]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
+ Response 200 (application/vnd.mason+json)

    + Body
    
        {
            {
            "manufacturer": "Volkswagen",
            "model": "Jetta",
            "year": 2008,
            "paymentplans": [
                {
                "provider": "JussinAutopiste",
                "totalprice": 12341.0,
                "key": "jussinautopistejetta"
                }
            ]
            }
        }

### Posts a new model to the collection[POST]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
    + Body
    
        {
        "manufacturer": "Toyota",
        "model": "Corolla",
        "year": 2000
        }
        
+ Response 200 (application/vnd.mason+json)


## Model Item[/{handle}/{model}]

Individual model item for inspection and editing

+ Parameters

    + handle(string) - A handle for grouping sets of paymentplans(handle)
    
    + model(string) - Name of the model(key)

### Gives the information about a model for inspection and editing [GET]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
+ Response 200 (application/vnd.mason+json)

    + Body
    
            {
            "manufacturer": "Volkswagen",
            "model": "Jetta",
            "year": 2008,
            "paymentplans": [
                {
                "provider": "JussinAutopiste",
                "totalprice": 12341.0,
                "key": "jussinautopistejetta"
                }
            ]
            }

### Modifies the model [PUT]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
    + Body
    
        {
            "manufacturer": "Volkswagen",
            "model": "Jetta",
            "year": 2010
        }
        
+ Response 200 (application/vnd.mason+json)


### Deletes the model [DELETE]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
+ Response 200 (application/vnd.mason+json)


## Paymentplan[/{handle}/item/{key}]

Individual Paymentplan for inspection and editing

+ Parameters

    + handle(string, unique) - A handle for grouping sets of paymentplans(handle)
    
    + key(string) - unique key to identify paymentplan(key)

### Gives the information about the paymentplan for inspection and editing [GET]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
+ Response 200 (application/vnd.mason+json)

    + Body
    
        {
        "price": 10123.0,
        "provider": "JormanAuto",
        "interestrate": 5.5,
        "months": 6,
        "payers": 2,
        "open": False,
        "carmodel": {
                    "manufacturer": "Toyota",
                    "model": "Corolla",
                    "year": 2010,
                    }
        }
        
        
### Modifies the paymentplan [PUT]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
    + Body
    
        {
        "price": 123123.0,
        "provider": "Peetu",
        "interestrate": 4.5,
        "months": 4,
        "payers": 2,
        "open": False,
        "carmodel": "toyotacorolla"
        }
        
+ Response 200 (application/vnd.mason+json)


### Deletes the model [DELETE]

+ request

    + headers 
    
        Accept: application/vnd.mason+json
        
+ Response 200 (application/vnd.mason+json)

