# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.post_save_code'
        db.add_column(u'questionnaire_question', 'post_save_code',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Question.post_save_code'
        db.delete_column(u'questionnaire_question', 'post_save_code')


    models = {
        u'questionnaire.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.Question']"}),
            'runid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.Subject']"})
        },
        u'questionnaire.choice': {
            'Meta': {'object_name': 'Choice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.Question']"}),
            'sortid': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'text_pl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'questionnaire.question': {
            'Meta': {'object_name': 'Question'},
            'checks': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'extra_pl': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'footer_pl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'post_save_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'questionset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.QuestionSet']"}),
            'text_pl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'redirect_url': ('django.db.models.fields.CharField', [], {'default': "'/static/complete.html'", 'max_length': '128'})
        },
        u'questionnaire.questionset': {
            'Meta': {'object_name': 'QuestionSet'},
            'checks': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.Questionnaire']"}),
            'sortid': ('django.db.models.fields.IntegerField', [], {}),
            'text_pl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'questionnaire.runinfo': {
            'Meta': {'object_name': 'RunInfo'},
            'cookies': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'emailcount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'emailsent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastemailerror': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'questionset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.QuestionSet']", 'null': 'True', 'blank': 'True'}),
            'random': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'runid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'skipped': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.Subject']"}),
            'tags': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'questionnaire.runinfohistory': {
            'Meta': {'object_name': 'RunInfoHistory'},
            'completed': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.Questionnaire']"}),
            'runid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'skipped': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questionnaire.Subject']"}),
            'tags': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'questionnaire.subject': {
            'Meta': {'object_name': 'Subject'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'formtype': ('django.db.models.fields.CharField', [], {'default': "'email'", 'max_length': '16'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'unset'", 'max_length': '8', 'blank': 'True'}),
            'givenname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '2'}),
            'nextrun': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'inactive'", 'max_length': '16'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['questionnaire']