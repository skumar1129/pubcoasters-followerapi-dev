from src.models.post import Post

class PostResponse():

    def __init__(self, uuid, pic_link, bar, location, description, rating, anonymous, created_at, edited_at, likes=None, num_likes=None, comments=None, num_comments=None, neighborhood=None, created_by=None):
        self.response = {
            'uuid': uuid,
            'picLink': pic_link,
            'bar': bar,
            'description': description,
            'location': location,
            'rating': rating,
            'anonymous': anonymous,
            'createdAt': created_at,
            'editedAt': edited_at
        }
        if comments is not None:
            self.response['comments'] = comments
        elif num_comments is not None:  
            self.response['numComments'] = num_comments
        if neighborhood is not None:
            self.response['neighborhood'] = neighborhood
        if created_by is not None:
            self.response['createdBy'] = created_by
        if likes is not None:
            self.response['likes'] = likes
        elif num_likes is not None:
            self.response['numLikes'] = num_likes