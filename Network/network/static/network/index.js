document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('#profile') != null) {
        document.querySelector('#profile').addEventListener('click', () => view_profile(document.querySelector('#profile').textContent));
        document.querySelector('#following').addEventListener('click', () => load_feed('following'));
        document.querySelector('#post-form').onsubmit = () => {
            make_post();
        };
    }

    document.querySelector('#all').addEventListener('click', () => load_feed('all'));

    load_feed('all');
});

function make_post() {

    fetch('/posts', {

        method: 'POST',
        body: JSON.stringify({
          body: document.querySelector('#post-body').value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}

function edit_post(post_id) {

    console.log('edited post: ' + post_id);

    fetch('/posts/edit/' + post_id, {

        method: 'POST',
        body: JSON.stringify({
          body: document.querySelector('#edit-body' + post_id).value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}

function load_feed(feed) {
    console.log('appleseed')
    if(feed == 'all') {
        document.querySelector('#header').innerHTML = "All Posts";
    } else if (feed == 'following') {
        document.querySelector('#header').innerHTML = "Following";
    }

    document.querySelector('#seeposts').innerHTML = '';
    document.querySelector('#profile-div').innerHTML = '';

    fetch('/posts/' + feed, {

        method: 'GET',
        headers: {
          'accept-encoding': 'none',
          'content-type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(postPages => {
        console.log(postPages);
        load_page(feed, postPages, 0);
    });
}

function load_page(feed, posts, page) {
    console.log('in load_page')
    document.querySelector('#seeposts').innerHTML = '';

    if (posts !== undefined || posts.length > 0) {
        postsPage = posts[page];
        console.log(postsPage);
        postsPage.forEach(post => {

            const postDiv = document.createElement('div');
            postDiv.id = 'post';

            const postUser = document.createElement('h4');
            postUser.textContent = post.user;
            postDiv.append(postUser);
            postUser.addEventListener('click', () => {
                view_profile(post.user);
            })

            const form = document.querySelector('#post-form').cloneNode(true);
            editFormId = 'edit-form' + post.id;
            form.id = editFormId;
            form.style.display = 'none';
            form.querySelector('textarea').id = 'edit-body' + post.id;
            form.querySelector('input').value = 'Edit';
            form.onsubmit = () => {
                console.log("hey")
                edit_post(post.id);
            };
            postDiv.append(form);

            if (document.querySelector('#profile') != null && post.user == document.querySelector('#profile').textContent) {
                const edit = document.createElement('p');
                edit.id = 'edit'
                edit.textContent = 'Edit'
                edit.addEventListener('click', () => {

                    console.log(16)
                    edit.style.display = 'none';
                    postBody.style.display = 'none';
                    document.querySelector('#edit-form' + post.id).style.display = 'block';
                });
                postDiv.append(edit);
            }
            console.log(post.body)
            const postBody = document.createElement('p');
            postBody.textContent = post.body;
            postDiv.append(postBody);

            const postTime = document.createElement('p');
            postTime.id = 'postInfo';
            postTime.textContent = post.timestamp;
            postDiv.append(postTime);

            const likes = document.createElement('p');

            numLikes = post.likes.length;
            likes.textContent = `🧡 ` + numLikes;
            postDiv.append(likes);

            const like = document.createElement('p');
            like.id = 'likeButton'
            like.textContent = 'Like!'
            like.addEventListener('click', () => {

                console.log(18);
                like_post(post.id);
                fetch('/posts/get/' + post.id, {

                    method: 'GET'
                })
                .then(response => response.json())
                .then(() => {
                    load_page(feed,posts,page);
                });
            });
            postDiv.append(like);

            const unlike = document.createElement('p');
            unlike.id = 'likeButton';
            unlike.textContent = 'Unlike.'
            unlike.addEventListener('click', () => {

                console.log(19)
                unlike_post(post.id);

                fetch('/posts/get/' + post.id, {

                    method: 'GET'
                })
                .then(response => response.json())
                .then(() => {
                    load_page(feed,posts,page);
                });
            });
            postDiv.append(unlike);

            

            if (document.querySelector('#profile') != null) {
                fetch('/posts/haveliked/' + post.id, {

                    method: 'GET',
                    headers: {
                        'accept-encoding': 'none',
                        'content-type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(liked => {
                    console.log(post.id);
                    console.log(liked);
                    console.log(liked == true);

                    if (liked.liked) {

                        console.log(12)
                        like.style.display = 'none';
                        unlike.style.display = 'block';
                    } else {
                        console.log(13)
                        unlike.style.display = 'none';
                        like.style.display = 'block';
                    }
                });
            } else {
                unlike.style.display = 'none';
                like.style.display = 'none';
            }

            document.querySelector('#seeposts').append(postDiv);

        })

        if (posts.length > 0) {

            pageNav = document.createElement('nav');
            
            navButtons = document.createElement('ul');

            if (page != 0) {
                
                prevButton = document.createElement('button');
                prevButton.textContent = "Previous";
                prevButton.addEventListener('click', () => {
                    load_page(feed, posts, page-1);
                })
                prevButton.className = 'navigation';
                navButtons.append(prevButton);
            }
            
            if (page != posts.length-1) {
               
                nextButton = document.createElement('button');
                nextButton.textContent = 'Next';
                nextButton.addEventListener('click', () => {
                    load_page(feed, posts, page+1);
                })
                nextButton.className = 'navigation';
                navButtons.append(nextButton);
            }
            pageNav.append(navButtons);

            document.querySelector('#seeposts').append(pageNav);
        }
    } else {

        const postDiv = document.createElement('div');
        postDiv.textContent = 'No posts yet. Be the first to post!';

        document.querySelector('#seeposts').append(postDiv);
    }
}

function like_post(post_id) {

    console.log(post_id);

    fetch('/posts/like/' + post_id, {

        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}

function unlike_post(post_id) {

    console.log(post_id);

    fetch('/posts/unlike/' + post_id, {

        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}

function view_profile(username) {

    document.querySelector('#header').innerHTML =  username + '\'s Profile';

    document.querySelector('#seeposts').innerHTML = '';
    document.querySelector('#profile-div').innerHTML = '';
    
    fetch('/posts/isfollowing/' + username, {
        method: 'GET',
        headers: {
            'accept-encoding': 'none',
            'content-type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(following => {
        console.log('following ...')
        console.log(following)
        if (following.following != 'same') {
            if (!following.following) {
            
                const follow = document.createElement('p');
                follow.id = 'followButton';
                follow.textContent = 'Follow!'
                follow.addEventListener('click', () => {
        
                    fetch('/posts/follow/' + username, {
                        method: 'POST',
                    })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result);
                    });
                });
                document.querySelector('#profile-div').append(follow);
            } else {
    
                const unfollow = document.createElement('p');
                unfollow.id = 'unfollowButton';
                unfollow.textContent = 'Unfollow.'
                unfollow.addEventListener('click', () => {
    
                    fetch('/posts/unfollow/' + username, {
                        method: 'POST',
                    })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result);
                    });
                });
                document.querySelector('#profile-div').append(unfollow);
            }
        }
        
    })

    load_feed(username);
}