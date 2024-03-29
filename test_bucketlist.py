import unittest
from flask import json
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = { 'name': 'Go to Kampala for vacation'}


        #bind the app to the current context
        with self.app.app_context():
            #create all tables
            db.create_all()

    def test_bucketlist_creation(self):
        """Test API can create a bucket list(POST request)"""
        res = self.client().post('/bucketlists/',  data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go to Kampala for vacation', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)."""
        res = self.client().post('/bucketlists/', content_type='application/json',
        data=json.dumps(
            dict(
              name=self.bucketlist['name']  
            )
        ))
        self.assertEqual(res.status_code, 201)
        get_response = self.client().get('/bucketlists/')
        self.assertEqual(get_response.status_code, 200)
        self.assertIn('Go to Kampala for vacation', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        rv = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        result = self.client().get(
            '/bucketlists/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Kampala for vacation', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/bucketlists/1',
            content_type='application/json',
            data= json.dumps(
                dict(
                    name= 'Dont just eat, but also pray and love'
                )
            ))
        self.assertEqual(rv.status_code, 200)

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)."""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        get_list = self.client().get('/buckelists/')
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()