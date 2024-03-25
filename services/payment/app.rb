##
# The PaymentApp class is a Sinatra application that handles payment processing.
# It provides two routes: a GET route at "/" that returns a greeting message,
# a GET route at "/session" that retrieves a Stripe Checkout session and its associated PaymentIntent,
# and a POST route at "/make_payment" that creates a new Stripe Checkout session for a payment.
#
# Environment Variables:
# - STRIPE_SECRET_KEY: The secret key for the Stripe API.
#
# Routes:
# - GET "/": Returns a greeting message.
# - GET "/session": Retrieves a Stripe Checkout session and its associated PaymentIntent.
#   The session ID should be provided as a query parameter.
# - POST "/make_payment": Creates a new Stripe Checkout session for a payment.
#   The request body should be a JSON object with a "line_items" property that is an array of objects,
#   each with a "price" and "quantity" property.
#
# Each route returns a JSON object with a "status" property that is either "success" or "error".
# If the status is "success", the object will also include additional data about the request.
# If the status is "error", the object will include a "message" property with a description of the error.


require 'sinatra'

set :port, 9292

require 'stripe'
require 'json'
require 'dotenv'
require 'sinatra/reloader' if development?

Dotenv.load
Stripe.api_key = ENV['STRIPE_SECRET_KEY']


class PaymentApp < Sinatra::Base
    configure :development do
        register Sinatra::Reloader
      end

    
  get '/' do
    'Hello from Payment service'
    end

    get "/session" do
        session = params[:session]
        session = Stripe::Checkout::Session.retrieve(session)
        payment_intent = Stripe::PaymentIntent.retrieve(session.payment_intent)
      
        [200, { 'Content-Type' => 'application/json' }, { status: 'success', session: session, payment_intent: payment_intent }.to_json]
      rescue => e
        [500, { 'Content-Type' => 'application/json' }, { status: 'error', message: e.message }.to_json]
      end
    
  post '/make_payment' do
    begin
      payload = JSON.parse(request.body.read)
      line_items = payload['line_items']  # This should be an array of objects, each with a 'price' and 'quantity' property

      checkout = Stripe::Checkout::Session.create({
        success_url: 'http://10.83.7.252:3000/successpayment',
        cancel_url: 'https://example.com/cancel',
        payment_method_types: ['card'],
        line_items: line_items,
        mode: 'payment',
      })
      

      [200, { 'Content-Type' => 'application/json' }, { status: 'success', session_id: checkout.id, url: checkout.url }.to_json]
  rescue => e
    [500, { 'Content-Type' => 'application/json' }, { status: 'error', message: e.message }.to_json]
  end
end

    post '/refund' do
    begin
        payload = JSON.parse(request.body.read)
        session = payload['session']  # This should be the ID of the session

        # Retrieve the session and the associated payment intent
        session = Stripe::Checkout::Session.retrieve(session)
        payment_intent_id = session.payment_intent

        refund = Stripe::Refund.create({
        payment_intent: payment_intent_id,
      
        })

        [200, { 'Content-Type' => 'application/json' }, { status: 'success', refund: refund }.to_json]
    rescue => e
        [500, { 'Content-Type' => 'application/json' }, { status: 'error', message: e.message }.to_json]
    end
    end

    post '/partialRefund' do
      begin
          payload = JSON.parse(request.body.read)
          session = payload['session']  # This should be the ID of the session
          amount = payload['amount']  # This should be the amount to refund in cents
  
          # Retrieve the session and the associated payment intent
          session = Stripe::Checkout::Session.retrieve(session)
          payment_intent_id = session.payment_intent
  
          refund = Stripe::Refund.create({
          payment_intent: payment_intent_id,
          amount: amount,
          })
  
          [200, { 'Content-Type' => 'application/json' }, { status: 'success', refund: refund }.to_json]
      rescue => e
          [500, { 'Content-Type' => 'application/json' }, { status: 'error', message: e.message }.to_json]
      end
      end

  post '/stripe_webhook' do
    payload = request.body.read
    sig_header = request.env['HTTP_STRIPE_SIGNATURE']
    event = nil

    begin
      event = Stripe::Webhook.construct_event(
        payload, sig_header, ENV['STRIPE_WEBHOOK_SECRET']
      )
    rescue JSON::ParserError => e
      return [400, { 'Content-Type' => 'application/json' }, { status: 'error', message: 'Invalid payload' }.to_json]
    rescue Stripe::SignatureVerificationError => e
      return [400, { 'Content-Type' => 'application/json' }, { status: 'error', message: 'Invalid signature' }.to_json]
    end

    # Handle the event
    case event.type
    when 'charge.succeeded'
      # Handle successful charge
    when 'charge.failed'
      # Handle failed charge
    end

    [200, { 'Content-Type' => 'application/json' }, { status: 'success' }.to_json]
  end
end

# At the end of app.rb
PaymentApp.run! if __FILE__ == $0