"""
This file is used to configure application settings.

Do not import this file directly.

You can use the settings API via:

    from ferris import settings

    mysettings = settings.get("mysettings")

The settings API will load the "settings" dictionary from this file. Anything else
will be ignored.

Optionally, you may enable the dynamic settings plugin at the bottom of this file.
"""

settings = {}

settings['timezone'] = {
    'local': 'US/Eastern'
}

settings['email'] = {
    # Configures what address is in the sender field by default.
    'sender': None
}

settings['app_config'] = {
    'webapp2_extras.sessions': {
        # WebApp2 encrypted cookie key
        # You can use a UUID generator like http://www.famkruithof.net/uuid/uuidgen
        'secret_key': '9a788030-837b-11e1-b0c4-0800200c9a66',
    }
}

settings['oauth2'] = {
    # OAuth2 Configuration should be generated from
    # the google cloud console (Credentials for Web Application)
    'client_id': None,  # XXXXXXXXXXXXXXX.apps.googleusercontent.com
    'client_secret': None,
    'developer_key': None  # Optional
}

settings['oauth2_service_account'] = {
    # OAuth2 service account configuration should be generated
    # from the google cloud console (Service Account Credentials)
    'client_email': '573875402141-86k8t1hflu3meacqm8kngdd7o2ndffat@developer.gserviceaccount.com',  # XXX@developer.gserviceaccount.com
    'domain' : 'cloudsherpas.com',
    'private_key':  """-----BEGIN PRIVATE KEY-----
                    MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALZUYXTfoSO+1UyC
                    FEDcizpO5ekDxhfycalaNHU76vvBqMZZD8n2S+npwEIrbnRivVw389ZuV25patll
                    kHdb/3vyk0QAURJT3lCb/d7XeZE1EewDRHQqT+0P52DoRGpmHomFDEL2dl3Ox6yG
                    Pqht8YwYhYZxXrkm+HjqA/IXTCdbAgMBAAECgYBxTaJ6VHX4lqBKOROI8wR6KYlp
                    8fRp8Tl8uhebOq7d4AyXpcTQBoRKSf41oHO1U57E7ehTOqKOdGf3zMunwL3UJZpn
                    bQ6JPgrzWmOutTGVYLJdf8o955hQ81fPkbhO6aQYXcwYWKydp098okq6KRIc8oiS
                    DZ/ufqvLtyJQW1DoAQJBAOOfE6yGYnDLZc5pEZwiLBGbShwBeKPS96oLlPOhjTg8
                    eK38YCBEhz8RuKQbfjt180eqvj4JBGCMUCc1pJAvpVsCQQDND71fvDcLA2uBQ4fR
                    OIcUp8l6fevPxJOqrASeqIRvYDyNkHUKygSZj1UXDmF6DW4RTQGDpMg7g73U7ys1
                    gyYBAkBy7kidzUD5WQovncfBgVOlFDboSynh9k0NNEnidkj7AzWgDBVxVYjApK8J
                    VcR4O4c6QZFLe3wVT+PM2H4eO6CPAkBtm1onz9zEAEH4R/ZSuJpLShwBY0kmNvaP
                    JX8apwyS06fKK0rER5MJ2Xkr573mlUMd8EE88lksppBTPruj0MQBAkEA0lKM7Qcu
                    OYIYRtsmzWtQSGHivX+9k9tfAZYToyNGxgw53MOmgZCrY+yaI2wctCvEPHy19vfv
                    z7UjZDS21H9eOQ==
                    -----END PRIVATE KEY-----""",  # Must be in PEM format
    'DEVELOPER_KEY' : 'AIzaSyCZwjbsE2vKtCKAmsrN4VTwNKNGk8q2PaU'
}

settings['upload'] = {
    # Whether to use Cloud Storage (default) or the blobstore to store uploaded files.
    'use_cloud_storage': True,
    # The Cloud Storage bucket to use. Leave as "None" to use the default GCS bucket.
    # See here for info: https://developers.google.com/appengine/docs/python/googlecloudstorageclient/activate#Using_the_Default_GCS_Bucket
    'bucket': None
}

# Enables or disables app stats.
# Note that appstats must also be enabled in app.yaml.
settings['appstats'] = {
    'enabled': False,
    'enabled_live': False
}

# Optionally, you may use the settings plugin to dynamically
# configure your settings via the admin interface. Be sure to
# also enable the plugin via app/routes.py.

#import plugins.settings

# import any additional dynamic settings classes here.

# import plugins.my_plugin.settings

# Un-comment to enable dynamic settings
#plugins.settings.activate(settings)
