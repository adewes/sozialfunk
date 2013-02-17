# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Profile.first_name'
        db.delete_column('profiles_profile', 'first_name')

        # Deleting field 'Profile.last_name'
        db.delete_column('profiles_profile', 'last_name')

        # Deleting field 'Profile.has_verified_email'
        db.delete_column('profiles_profile', 'has_verified_email')

        # Deleting field 'Profile.twitter_username'
        db.delete_column('profiles_profile', 'twitter_username')

        # Deleting field 'Profile.has_beta_key'
        db.delete_column('profiles_profile', 'has_beta_key')

        # Deleting field 'Profile.has_verified_name'
        db.delete_column('profiles_profile', 'has_verified_name')

        # Adding field 'Profile.twitter_name'
        db.add_column('profiles_profile', 'twitter_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)

        # Adding field 'Profile.twitter_screen_name'
        db.add_column('profiles_profile', 'twitter_screen_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Profile.first_name'
        db.add_column('profiles_profile', 'first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)

        # Adding field 'Profile.last_name'
        db.add_column('profiles_profile', 'last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)

        # Adding field 'Profile.has_verified_email'
        db.add_column('profiles_profile', 'has_verified_email', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Profile.twitter_username'
        db.add_column('profiles_profile', 'twitter_username', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'Profile.has_beta_key'
        db.add_column('profiles_profile', 'has_beta_key', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Profile.has_verified_name'
        db.add_column('profiles_profile', 'has_verified_name', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Profile.twitter_name'
        db.delete_column('profiles_profile', 'twitter_name')

        # Deleting field 'Profile.twitter_screen_name'
        db.delete_column('profiles_profile', 'twitter_screen_name')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 14, 22, 1, 28, 676699)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 14, 22, 1, 28, 676379)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'appearance_on_platform': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'notification_policy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'notification_time': ('django.db.models.fields.TimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'notification_weekday': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_access_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'twitter_access_token_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'twitter_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'twitter_screen_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'unique_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['profiles']
