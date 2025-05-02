from flask import render_template, session, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.auth.forms import ImageUploadForm
from ..models import Image
from . import admin

import os
from werkzeug.utils import secure_filename


# Route: Admin Dashboard
@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not session.get('is_admin'):
        flash('Access denied. Admins only!', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))

    # We don't need 'images' here, as it only belongs in 'manage_images'
    return render_template('admin/admin.html')


# Route: Admin Manages Images
@admin.route('/manage_images', methods=['GET', 'POST'])
@login_required
def manage_images():
    if not session.get('is_admin'):
        flash('Access denied. Admins only!', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))

    form = ImageUploadForm()
    images = Image.query.all()  # Query all images to display in the table

    if form.validate_on_submit():
        image_file = form.image.data
        image_filename = secure_filename(image_file.filename)

        # Save the file
        image_file_path = os.path.join('static/images', image_filename)
        image_file.save(image_file_path)

        # Save metadata to DB
        new_image = Image(image_file=image_filename, description=form.description.data)
        db.session.add(new_image)
        db.session.commit()

        flash('Image uploaded successfully!', 'success')
        return redirect(url_for('admin.manage_images'))  # Refresh the page after success

    return render_template('admin/admin.html', form=form, images=images)  # Pass form and images


# Route: Delete Image
@admin.route('/delete_image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    if not session.get('is_admin'):
        flash('Access denied. Admins only!', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))

    image = Image.query.get(image_id)
    if image:
        try:
            # Remove the image file from the disk
            os.remove(os.path.join('static/images', image.image_file))
        except Exception as e:
            flash(f'Error deleting the image file: {e}', 'danger')

        # Delete the image record from the database
        db.session.delete(image)
        db.session.commit()
        flash('Image deleted successfully!', 'success')
    else:
        flash('Image not found!', 'danger')

    return redirect(url_for('admin.manage_images'))
