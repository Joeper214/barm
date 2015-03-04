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
    'client_email': '990820776391-pg5feb011an9083uqq897ad6i38jjpnd@developer.gserviceaccount.com',  # XXX@developer.gserviceaccount.com
    'domain' : 'sherpademo.com',
    'private_key':  """-----BEGIN PRIVATE KEY-----
                    MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBANmJWmnrkW6Mqw6m
                    GVc9HSZ4cCmXZNugTSvJclEQzCnDSOwL6fdRjuIlvCttsIIAsK0Kqsec9AsD5j4t
                    0OXbhFRDi9Irdce7VCDstGtk2Byn5/UixJXHgnO1n9C1c5W9tVWq2CKQcXc41OaF
                    /sfqrAfBxsScPd+ywj+Q6hRyUALLAgMBAAECgYEAoB23TOs1GnezmI6tbEbxY9WW
                    SSbD99wfsTEPUZfZjovM6uFCDuYbE13PCPAt0SKM6HFHjrF593mhSPcUIXvYA4mm
                    gxH5uBvPe1xlTOwRyT6oMQM5jFhUN5i3JLCXSRoZ4mnlDnDa0H+Yt60iEperV/dk
                    rhCfQ+qjw0ws54V8KTECQQD8BFN13LP5FVngdwW8Rzk/n1imtY8+KUZjUxg3WKnO
                    yYZ3VvIMlg5DJnbBbxntvZT2vwk9GdILUjbS+iGU98LHAkEA3PmEi2RxFHQALw+c
                    nFW3+6QuKlaWcTry2rqGq/U7mEtzIt1ZdDHX8tHcCCRk9vzoGyxilAt1LxN9nQsX
                    JC873QJAcu2KHiLTFFFvVlUREYatjd0eMZB0zZVHGz6muX6+maX/o2bMJX8869Sb
                    raT7/xZI26nNDcc7qZwJknctX2EJuwJANSmWmM6OYgRScwAHhpkczV6/eJIiWZV8
                    DeFoOwCh2M72IUItnkXLlXClxhOzcrR/xuHTyZhEFhJTWy/q3lq6xQJAYyalbAz4
                    ouaHlhYwgTbw/RO65pAnqqibafS0d6X4BzEFCd+6Nragx6dAV1FHC900vZip03W/
                    3hD5MFTzu4JhWQ==
                    -----END PRIVATE KEY-----""",  # Must be in PEM format
    'DEVELOPER_KEY' : 'AIzaSyA3UKNHd6a7gys4pYri08mEFWt-0MXutZc'
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
