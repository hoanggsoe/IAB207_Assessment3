from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from .models import Event, Comment, Order, User
from .forms import EventForm, CommentForm, BookingForm
from . import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)

def update_event_status():
    events = Event.query.all()
    for event in events:
        if event.date < datetime.now() and event.status == 'Open':
            event.status = 'Inactive'
        elif event.tickets_available <= 0 and event.status == 'Open':
            event.status = 'Sold Out'
    db.session.commit()

@main_bp.route('/') # Main route for the homepage
def index():
    update_event_status()
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Event.query
    
    if category and category != 'All':
        query = query.filter(Event.category == category)
    
    if search:
        query = query.filter(
            (Event.name.contains(search)) | 
            (Event.description.contains(search))
        )
    
    events = query.order_by(Event.date.asc()).all()
    categories = ['Jazz', 'Rock', 'Hip-Hop', 'Electronic', 'Classical', 'Pop', 'Reggae', 'Acoustic']
    
    return render_template('index.html', events=events, categories=categories, selected_category=category)

@main_bp.route('/event/<int:id>') # Route for event details
def event_detail(id):
    event = Event.query.get_or_404(id)
    comment_form = CommentForm()
    booking_form = BookingForm()
    comments = Comment.query.filter_by(event_id=id).order_by(Comment.created_at.desc()).all()
    
    return render_template('event.html', event=event, comment_form=comment_form, 
                         booking_form=booking_form, comments=comments)

@main_bp.route('/event/<int:id>/comment', methods=['POST']) # Route to add a comment to an event
@login_required
def add_comment(id):
    event = Event.query.get_or_404(id)
    comment_form = CommentForm()
    
    if comment_form.validate_on_submit():
        comment = Comment(
            content=comment_form.content.data,
            user_id=current_user.id,
            event_id=id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted successfully!', 'success')
    else:
        flash('Please enter a valid comment.', 'error')
    
    return redirect(url_for('main.event_detail', id=id))

@main_bp.route('/event/<int:id>/book', methods=['POST'])# Route to book tickets for an event
@login_required
def book_tickets(id):
    event = Event.query.get_or_404(id)
    booking_form = BookingForm()
    
    if event.status != 'Open':
        flash('This event is not available for booking.', 'error')
        return redirect(url_for('main.event_detail', id=id))
    
    if booking_form.validate_on_submit():
        quantity = booking_form.quantity.data
        
        if quantity > event.tickets_available:
            flash(f'Only {event.tickets_available} tickets available.', 'error')
            return redirect(url_for('main.event_detail', id=id))
        
        total_cost = quantity * event.price
        
        order = Order(
            quantity=quantity,
            total_cost=total_cost,
            user_id=current_user.id,
            event_id=id
        )
        
        event.tickets_available -= quantity
        if event.tickets_available <= 0:
            event.status = 'Sold Out'
        
        db.session.add(order)
        db.session.commit()
        
        flash(f'Successfully booked {quantity} tickets! Order ID: {order.id}', 'success')
    
    return redirect(url_for('main.event_detail', id=id))

@main_bp.route('/create', methods=['GET', 'POST']) # Route to create a new event
@login_required
def create_event():
    form = EventForm()
    
    if form.validate_on_submit():
        image_filename = 'default_event.jpg'
        if form.image.data:
            image_filename = secure_filename(form.image.data.filename)
            image_path = os.path.join('website/static/img', image_filename)
            form.image.data.save(image_path)
        
        event = Event(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data,
            venue=form.venue.data,
            category=form.category.data,
            price=form.price.data,
            tickets_available=form.tickets_available.data,
            image=image_filename,
            user_id=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('main.event_detail', id=event.id))
    
    return render_template('create.html', form=form)

@main_bp.route('/event/<int:id>/edit', methods=['GET', 'POST'])# Route to edit an existing event
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    
    if event.user_id != current_user.id:
        flash('You can only edit your own events.', 'error')
        return redirect(url_for('main.event_detail', id=id))
    
    form = EventForm(obj=event)
    
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.date = form.date.data
        event.venue = form.venue.data
        event.category = form.category.data
        event.price = form.price.data
        event.tickets_available = form.tickets_available.data
        
        if form.image.data:
            image_filename = secure_filename(form.image.data.filename)
            image_path = os.path.join('website/static/img', image_filename)
            form.image.data.save(image_path)
            event.image = image_filename
        
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('main.event_detail', id=id))
    
    return render_template('create.html', form=form, event=event)

@main_bp.route('/event/<int:id>/cancel')# Route to cancel an event
@login_required
def cancel_event(id):
    event = Event.query.get_or_404(id)
    
    if event.user_id != current_user.id:
        flash('You can only cancel your own events.', 'error')
        return redirect(url_for('main.event_detail', id=id))
    
    event.status = 'Cancelled'
    db.session.commit()
    
    flash('Event cancelled successfully.', 'info')
    return redirect(url_for('main.event_detail', id=id))

@main_bp.route('/history')# Route to view booking history
@login_required
def booking_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.timestamp.desc()).all()
    return render_template('history.html', orders=orders)


