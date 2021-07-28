from flask import request, jsonify
from src.app import db
from src.models.post import Post
from src.models.neighborhood import Neighborhood
from src.models.location import Location
from src.models.rating import Rating
from src.models.bar import Bar
from src.models.likes import Likes
from src.models.comment import Comment
from src.models.user import User
from src.models.follower import Follower
from src.response.post_response import PostResponse


class FollowerService():

    def createFollowing(self, body):
        try:
            follower = body['follower']
            following = body['following']
            if follower != following:
                new_following = Follower(follower_user=follower, following_user=following)
                db.session.add(new_following)
                db.session.commit()
                return jsonify({'message': 'successfully created following'}), 200
            else:
                return jsonify({'message': 'user can not follow themselves'}), 500
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to creating new following'}), 500


    def deleteFollowing(self, body):
        try:
            follower = body['follower']
            following = body['following']
            old_following = Follower.query.filter_by(follower_user=follower, following_user=following).first()
            db.session.delete(old_following)
            db.session.commit()
            return jsonify({'message': 'successfully deleted following'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'unable to deleting following'}), 500

    def getAllFollowers(self, user, page):
        all_followers = []
        try:
            followers_data = Follower.query.filter_by(following_user=user).paginate(page=page, per_page=7)
            for follower_data in followers_data.items:
                follow = user in (obj.follower_user for obj in follower_data.follower[0].following)
                follower = {
                    'user': follower_data.follower_user,
                    'bio': ('' if follower_data.follower[0].bio is None else follower_data.follower[0].bio),
                    'fullName': follower_data.follower[0].full_name,
                    'picLink': ('' if follower_data.follower[0].link_to_prof_pic is None else follower_data.follower[0].link_to_prof_pic),
                    'following': follow
                }
                all_followers.append(follower)
            return jsonify(all_followers)
        except Exception as e:
            print(e)
            if (e.__str__() == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'):
                return jsonify(all_followers)
            return jsonify({'message': 'unable to retrieve followers'}), 500


    def getAllFollowing(self, user, page):
        all_following = []
        try:
            followings_data = Follower.query.filter_by(follower_user=user).paginate(page=page, per_page=7)
            for following_data in followings_data.items:
                following = {
                    'user': following_data.following_user,
                    'bio': ('' if following_data.following[0].bio is None else following_data.following[0].bio),
                    'fullName': following_data.following[0].full_name,
                    'picLink': ('' if following_data.following[0].link_to_prof_pic is None else following_data.following[0].link_to_prof_pic) 
                }
                all_following.append(following)
            return jsonify(all_following)
        except Exception as e:
            print(e)
            if (e.__str__() == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'):
                return jsonify(all_following)
            return jsonify({'message': 'unable to retrieve following'}), 500
    

    def getAllUserFollowers(self, user, my_user, page):
        all_followers = []
        try:
            followers_data = Follower.query.filter_by(following_user=user).paginate(page=page, per_page=7)
            for follower_data in followers_data.items:
                follow = my_user in (obj.follower_user for obj in follower_data.follower[0].following)
                follower = {
                    'user': follower_data.follower_user,
                    'bio': ('' if follower_data.follower[0].bio is None else follower_data.follower[0].bio),
                    'fullName': follower_data.follower[0].full_name,
                    'picLink': ('' if follower_data.follower[0].link_to_prof_pic is None else follower_data.follower[0].link_to_prof_pic),
                    'following': follow
                }
                all_followers.append(follower)
            return jsonify(all_followers)
        except Exception as e:
            print(e)
            if (e.__str__() == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'):
                return jsonify(all_followers)
            return jsonify({'message': 'unable to retrieve followers'}), 500

 

    def getAllUserFollowing(self, user, my_user, page):
        all_following = []
        try:
            followings_data = Follower.query.filter_by(follower_user=user).paginate(page=page, per_page=7)
            for following_data in followings_data.items:
                follow = ''
                follow = my_user in (obj.follower_user for obj in following_data.following[0].following)
                following = {
                    'user': following_data.following_user,
                    'bio': ('' if following_data.following[0].bio is None else following_data.following[0].bio),
                    'fullName': following_data.following[0].full_name,
                    'picLink': ('' if following_data.following[0].link_to_prof_pic is None else following_data.following[0].link_to_prof_pic),
                    'following': follow 
                }
                all_following.append(following)
            return jsonify(all_following)
        except Exception as e:
            print(e)
            if (e.__str__() == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'):
                return jsonify(all_following)
            return jsonify({'message': 'unable to retrieve following'}), 500
    


    def getFollowingPosts(self, user, page):
        all_following_posts = []
        post_count = 0
        try:
            post_data = Post.query.join(Follower, Follower.following_user == Post.created_by).filter_by(follower_user=user).join(Bar).join(Location).join(Rating).outerjoin(Neighborhood, Neighborhood.id == Post.neighborhood_id).order_by(Post.created_at.desc()).paginate(page=page, per_page=3)
            post_count = db.session.query(db.func.count(Post.id)).filter_by(anonymous = False).join(Follower, Follower.following_user == Post.created_by).filter_by(follower_user=user).scalar()
            for post in post_data.items:
                comments = db.session.query(db.func.count(Comment.post_id)).filter_by(post_id=post.id).scalar()
                likes = db.session.query(db.func.count(Likes.post_id)).filter_by(post_id=post.id).scalar()
                if (post.anonymous == False and post.neighborhood is not None):
                    return_post =  PostResponse(uuid=post.uuid, pic_link=post.pic_link, description=post.description, bar=post.bar.name, location=post.location.location, rating=post.rating.rating, anonymous=post.anonymous, created_at=post.created_at, edited_at=post.edited_at, num_comments=comments, num_likes=likes, neighborhood=post.neighborhood.neighborhood, created_by=post.created_by).response
                    all_following_posts.append(return_post)
                elif (post.anonymous == False and post.neighborhood is None):
                    return_post = PostResponse(uuid=post.uuid, pic_link=post.pic_link, description=post.description, bar=post.bar.name, location=post.location.location, rating=post.rating.rating, anonymous=post.anonymous, created_at=post.created_at, edited_at=post.edited_at, num_comments=comments, num_likes=likes, created_by=post.created_by).response
                    all_following_posts.append(return_post)
            return jsonify({'totalCount': post_count, 'posts': all_following_posts})
        except Exception as e:
            print(e)
            if (e.__str__() == '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'):
                return jsonify({'totalCount': post_count, 'posts': all_following_posts})
            return jsonify({'message': 'unable to retrieve posts'}), 500