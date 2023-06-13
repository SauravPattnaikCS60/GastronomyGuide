'''

This file performs a limited depth first search to get the recommendations given an user input

'''

def depth_limited_search(recommendation_model, source_restaurant, limit=2):
    restaurant_stack = []
    restaurant_stack.append(source_restaurant)
    depth = 0
    depth_stack = []
    depth_stack.append(depth)
    recommendations = []

    while (len(restaurant_stack) != 0):

        restaurant_popped = restaurant_stack.pop()
        curr_depth = depth_stack.pop()

        if curr_depth > limit or restaurant_popped in recommendations:
            continue

        restaurant_neighbours = [t[0] for t in recommendation_model[restaurant_popped]]
        depth = curr_depth + 1
        depth_stack = depth_stack + [depth] * len(restaurant_neighbours)
        restaurant_stack = restaurant_stack + restaurant_neighbours
        recommendations.append(restaurant_popped)

    recommendations.remove(source_restaurant)
    return recommendations