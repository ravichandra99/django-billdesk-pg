from distutils.core import setup
setup(
  name = 'django-billdesk-pg',         # How you named your package folder (MyLib)
  package_dir={'payments': 'payments'},
  packages = ['payments'],   # Chose the same as "name"
  include_package_data=True,
  version = '0.61',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Django BillDesk Payment Gateway',   # Give a short description about your library
  author = 'Ravi Chandra',                   # Type in your name
  author_email = 'ravichandra@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/ravichandra99',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ravichandra99/django-billdesk-pg/archive/refs/tags/v0.61.tar.gz',    # I explain this later on
  keywords = ['PAYMENT', 'GATEWAY', 'BILLDESK'],   # Keywords that define your package best
  install_requires=[
    'django-import-export',            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)