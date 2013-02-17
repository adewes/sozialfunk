# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Profile'
        db.create_table('profiles_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('unique_key', self.gf('django.db.models.fields.CharField')(default='', max_length=32, null=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('has_verified_name', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_verified_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_beta_key', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('twitter_username', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('twitter_access_token', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('appearance_on_platform', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('notification_policy', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('notification_weekday', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('notification_time', self.gf('django.db.models.fields.TimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['Profile'])


    def backwards(self, orm):
        
        # Deleting model 'Profile'
        db.delete_table('profiles_profile')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 14, 21, 21, 15, 299872)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 2, 14, 21, 21, 15, 299699)'}),
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
            'appearance_on_platform': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'has_beta_key': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_verified_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_verified_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'notification_policy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'notification_time': ('django.db.models.fields.TimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'notification_weekday': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_access_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'unique_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['profiles']
