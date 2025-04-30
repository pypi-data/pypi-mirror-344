print('''
1]mongo
2]show dbs
3]use test
4]db.createCollection("products");
5]db.products.insertOne({ name: 'Laptop', category: 'Electronics', price: 4000 });
6]db.products.insertMany([
  { name: 'Laptop', category: 'Electronics', price: 4000 },
  { name: 'Football', category: 'Games', price: 500 }
])
6]db.products.insertMany([ 
  {name: 'Headphones', category: 'Tech Gadgets', price: 2500}, 
  {name: 'Blender', category: 'Home Appliances', price: 3000}, 
  {name: 'Notebook', category: 'Stationary', price: 50}, 
  {name: 'T-shirt', category: 'Fashion', price: 800}, 
  {name: 'Gaming Mouse', category: 'Tech Gadgets', price: 1500}, 
  {name: 'Desk Lamp', category: 'Home Decor', price: 1200}, 
  {name: 'Backpack', category: 'Accessories', price: 1800}, 
  {name: 'Shoes', category: 'Fashion', price: 2500}, 
  {name: 'Water Bottle', category: 'Utilities', price: 300}, 
  {name: 'Tablet', category: 'Tech Gadgets', price: 20000} 
]);
7]db.products.find();
8]db.products.find({ name: 'Books' });
9]db.products.find({ price: { $lt: 20000 } });  ##$lt means lower than 2000 $gt grater than
10]db.products.updateOne(
  { name: 'Laptop' },             // Filter: find the product with the name 'Laptop'
  { $set: { price: 70000 } }      // Update: set the price to 70000
);
11]db.products.find({ name: 'Laptop' });
12] db.products.updateMany( 
  {category: 'Electronics'}, 
  {$set: {category: 'Tech Gadgets'}} 
);
13]db.products.find({category: 'Tech Gadgets'});
14]db.products.find({ 
  $or: [ 
    { category: 'Tech Gadgets' }, 
    { price: { $lt: 10000 } } 
  ] 
});
15]db.products.find({ 
  $and: [ 
    { category: 'Stationary' }, 
    { price: { $lt: 1000 } } 
  ] 
});
16]db.products.find({ 
  $nor: [ 
    { category: 'Tech Gadgets' }, 
    { price: { $gte: 50000 } } 
  ] 
});
16]db.products.deleteOne({name: 'Laptop'}); 
17]db.products.deleteMany({ category: 'Fashion' }); 

# show tables;

      ''')
