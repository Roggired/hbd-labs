db = connect( 'mongodb://localhost/mongo' );

db.createUser(
  {
    "user": "mongo",
    "pwd":  "mongo",
    "roles": [ { "role": "readWrite", "db": "mongo" } ]
  }
);

db.createCollection('Orders');
db.createCollection('Restaurant');
db.createCollection('Clients');

db.Restaurant.insertOne(
	{
		"_id": ObjectId("2d6ffcc5581c6c45eaf22a7d"),
		"name": "Отличная курочка",
		"phone": "5444485",
		"email": "hen@mail.ru",
		"founding_day": "30.04.2014",
		"address": "……"
	}
);

db.Clients.insertOne(
	{
		"_id": ObjectId("3cff2f49a426543451398e8e"),
		"name": "Иванова Инна Ивановна",
		"phone": "5824585",
		"email": "iii@mail.ru",
		"birthday": "30.04.2014",
		"login": "iii",
		"address": {
		        "city": "СПб",
		        "street": "Московский пр",
		        "building": "12"
		},
		"update_time": "30.04.2024 15:22:55"
	}
);

db.Orders.insertOne(
	{
		"_id": ObjectId('466cfe8accb82618613d606f'),
		"Restaurant_id": ObjectId('2d6ffcc5581c6c45eaf22a7d'),
		"client_id": ObjectId('3cff2f49a426543451398e8e'),
		"order_items": [],
		"total_bonus": 579,
		"cost": 1760,
		"payment": 1760,
		"bonus_for_visit": 60,
		"statuses": [
			{
				"Status": "finished",
				"time": "2024-03-29 10:25:18"
			},
			{
				"Status": "delivering",
				"time": "2024-03-29 09:28:14"
			},
			{
				"Status": "prepairyng",
				"time": "2024-03-29 08:51:12"
			},
			{
				"Status": "new",
				"time": "2024-03-29 08:21:53"
			}
		],
		"final_status": "finished",
		"update_ time": "2024-03-29T10:25:18.572+00:00"
	}
);
