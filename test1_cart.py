import requests
import json  # Для работы с JSON
import pytest


def test_get_cart():
    url = "http://localhost:8000/cart"
    data = {"Tests": "Test get cart."}
    
    response = requests.get(url, json=data)
    print("Client ask API and get answer.")
    print("Message send: " + json.dumps(data))
    print("Message receive: " + json.dumps(response.json()))
    assert data == response.json()


def test_clear_cart():
    url = "http://localhost:8000/cart"
    data = {"Tests": "Test clear cart."}
    
    response = requests.delete(url, json=data)
    print("Client ask API and get answer.")
    print("Message send: " + json.dumps(data))
    print("Message receive: " + json.dumps(response.json()))
    assert data == response.json()
    
def test_get_dish_in_cart():
    url = "http://localhost:8000/cart/dish"
    data = {"Tests": "Test get dish in cart."}
    
    response = requests.get(url, json=data)
    print("Client ask API and get answer.")
    print("Message send: " + json.dumps(data))
    print("Message receive: " + json.dumps(response.json()))
    assert data == response.json()
    
def test_post_dish_in_cart():
    url = "http://localhost:8000/cart/dish"
    data = {"Tests": "Test post dish in cart."}
    
    response = requests.post(url, json=data)
    print("Client ask API and get answer.")
    print("Message send: " + json.dumps(data))
    print("Message receive: " + json.dumps(response.json()))
    assert data == response.json()
    
def test_put_dish_in_cart():
    url = "http://localhost:8000/cart/dish"
    data = {"Tests": "Test put dish in cart."}
    
    response = requests.put(url, json=data)
    print("Client ask API and get answer.")
    print("Message send: " + json.dumps(data))
    print("Message receive: " + json.dumps(response.json()))
    assert data == response.json()