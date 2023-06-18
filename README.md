# GastronomyGuide
A restaurant recommendation system for Bangalore.

### How it works?
Input a restaurant that you like from the list of 3649 restaurants available and then watch the model
give recommendations for similar restaurants that you might like based on your input.

### Algorithm
It is a simple algorithmic model that is based on certain handcrafted features like distance proximity, cuisines
dishes offered, approximate price for two and more. For every pair of restaurants, it computes a score
that is based on the weighted average of the handcrafted features and is then stored on a recommendations dictionary.

To generate recommendations, Depth First Limited Search is applied on the recommendations dictionary.

### Features Used
- distance_score - Computes the distance between the two restaurants.
- online_order_score - Whether the restaurants offer online orders
- booking_table_score - Whether the restaurants offer the facility of booking table
- rating_score - How similar are their ratings
- votes_score - How many people have registered their reviews
- type_of_restaurant_score - How similar are the restaurant types(like cafe,casual dining)
- dishes_score - How similar are the dishes offered
- cuisines_score - How similar are the cuisines offered
- approx_cost_score - How close are the approximate price for two person
- reviews_score - How similar are their reviews

### Sources
Dataset - [Zomato Bangalore Dataset](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants)

[Background Image](https://www.pexels.com/photo/paper-lanterns-707670/)

### Note
I am constantly working on making more refined and intelligent recommendations.
Incase of any suggestions/feedback/issues feel free to drop me a mail.