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

db.Restaurant.insertMany(
[{
  "_id": ObjectId("7276e8cd0cf48b4cde123456"),
  "name": "Булочная №13",
  "phone": "5444485",
  "email": "bun@mail.ru",
  "founding_day": "30.04.2014",
  "menu": [
    {
      "_id": ObjectId("7276e8cd0cf48b4cded0087c"),
      "name": "ОВОЩИ ПО-МЕКСИКАНСКИ",
      "price": 60,
      "dish_category": "Закуски"
    },
    {
      "_id": ObjectId("7276e8cd0cf48b4cded0087d"),
      "name": "КУРИЦА",
      "price": 60,
      "dish_category": "Закуски"
    },
    {
      "_id": ObjectId("7276e8cd0cf48b4cded0087e"),
      "name": "РОЛЛ",
      "price": 120,
      "dish_category": "Закуски"
    }
  ],
  "update_time": {
    "$date": {
      "$numberLong": "1716544812000"
    }
  }
}]
);

db.Clients.insertMany(
[{
  "_id": ObjectId("727a81ce9a8cd1920741e258"),
  "name": "Иванова Инна Ивановна",
  "phone": "5824585",
  "birthday": "30.04.2014",
  "email": "iii@mail.ru",
  "login": "iii",
  "address": "Московский пр. 12",
  "update_time": {
    "$date": {
      "$numberLong": "1716544813000"
    }
  }
},{
  "_id": ObjectId("726a81ce9a8cd1920741e259"),
  "name": "Екатрина Романовна Дашкова",
  "phone": "5824587",
  "birthday": "01.01.1991",
  "email": "erd@mail.ru",
  "login": "kati17",
  "address": "Дворцовая набережная 38",
  "update_time": {
    "$date": {
      "$numberLong": "1716544813000"
    }
  }
}]
);

db.Orders.insertMany(
[
{
  "_id": ObjectId("772738ba5b1241c78abc7e17"),
  "restaurant": {
    "id": ObjectId("ef8c42c14b7518a4aebec107")
  },
  "order_date": {
    "$date": {
      "$numberLong": "1713780422100"
    }
  },
  "client": {
    "id": ObjectId("727a81ce4a8cd1420741e25e")
  },
  "ordered_dish": [
    {
      "id": ObjectId("770244ac855a44c5287cb2ac"),
      "name": "Масала",
      "price": 550,
      "quantity": 2
    },
    {
      "id": ObjectId("080d4248a4773012342b117a"),
      "name": "Карри",
      "price": 744,
      "quantity": 2
    },
    {
      "id": ObjectId("7b27444b845e2740c8774b47"),
      "name": "Чай",
      "price": 444,
      "quantity": 4
    }
  ],
  "payed_by_bonuses": 780,
  "cost": 8051,
  "payment": 8051,
  "bonus_for_visit": 374,
  "statuses": [
    {
      "status": "CLOSED",
      "time": "2024-04-22 10:15:22"
    },
    {
      "status": "DELIVERING",
      "time": "2024-04-22 04:22:14"
    },
    {
      "status": "COOKING",
      "time": "2024-04-22 04:11:20"
    },
    {
      "status": "OPEN",
      "order_date": "2024-04-22 08:28:33"
    }
  ],
  "final_status": "CLOSED",
  "update_time": {
    "$date": {
      "$numberLong": "1713780422100"
    }
  }
}
]);
