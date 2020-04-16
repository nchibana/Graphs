import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def get_friends(self, user_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.friendships[user_id]

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for user in range(num_users):
            self.add_user(user)

        # create a list with all possible friendship combinations
        friendships = []
        for user in range(1, self.last_id + 1):
            for friend in range(user + 1, num_users):
                friendships.append((user, friend))

        # shuffle the list, 
        # mutate in place with: random.shuffle(array)

        # or, Fisher-Yates shuffle!
        for idx in range(len(friendships)):
         # randint will give us an integer in this range, inclusive (includes last number)
            rand_idx = random.randint(0, len(friendships) - 1)  
            # I think this syntax for swapping items is sweet
            friendships[idx], friendships[rand_idx] = friendships[rand_idx], friendships[idx]

        # then grab the first N elements from the list.
        total_friendships = num_users * avg_friendships
        pairs_needed = total_friendships // 2 # bc add_friendship makes 2 at a time
        random_friendships = friendships[:pairs_needed]

        # Create friendships
        for friendship in random_friendships:
            self.add_friendship(friendship[0], friendship[1])


    def bfs(self, starting_user_id, destination_user_id):
        """
        Return a list containing the shortest friendship path from
        starting_user_id to destination_user_id in
        breath-first order.
        """
         # create an empty queue
        q = Queue()
        path = [starting_user_id]
        # enqueue the starting_vertex
        q.enqueue(path)
        # create a set to track vertices we have visited
        visited = set()
        # while the queue isn't empty:
        while q.size() > 0:
        ## dequeue, this is our current_node
            current_path = q.dequeue()
            current_id = current_path[-1]
            if current_id == destination_user_id:
                return current_path
        ## if we haven't visited it yet
            if current_id not in visited:
                visited.add(current_id)
                ## get its neighbors
                friends = self.get_friends(current_id)
                ## and add each to the back of queue
                for friend in friends:
                    path_copy = current_path[:]
                    path_copy.append(friend)
                    q.enqueue(path_copy)

    def bft(self, starting_user_id):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # create an empty queue
        q = Queue()
        # enqueue the starting_vertex
        q.enqueue(starting_user_id)
        # create a set to track vertices we have visited
        visited = set()
        # while the queue isn't empty:
        while q.size() > 0:
        ## dequeue, this is our current_node
            current_id = q.dequeue()
        ## if we haven't visited it yet
            if current_id not in visited:
                ## mark as visited
                visited.add(current_id)
                ## get its neighbors
                friends = self.get_friends(current_id)
                ## and add each to the back of queue
                for friend in friends:
                    q.enqueue(friend)
                    # return visited
        return visited

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        extended_network = self.bft(user_id)
        
        for friendship in extended_network:
            if friendship not in visited:
                visited[friendship] = self.bfs(user_id, friendship)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
