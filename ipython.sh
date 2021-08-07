#!/bin/sh

if ! test -d "$PROJECT_SOURCE" ; then
  PROJECT_SOURCE=$(git rev-parse --show-toplevel)
fi

# if test -n "$DISPLAY"; then
#   export QT_QPA_PLATFORM_PLUGIN_PATH=`echo ${pkgs.qt5.qtbase.bin}/lib/qt-*/plugins/platforms/`
#   alias ipython='ipython --matplotlib=qt5 --profile-dir=$CWD/.ipython-profile'
#   alias ipython0='ipython --profile-dir=$CWD/.ipython-profile'
# fi

mkdir $PROJECT_SOURCE/.ipython-profile 2>/dev/null || true
cat >$PROJECT_SOURCE/.ipython-profile/ipython_config.py <<EOF
c = get_config()
c.InteractiveShellApp.exec_lines = []
c.InteractiveShellApp.exec_lines.append('%load_ext autoreload')
c.InteractiveShellApp.exec_lines.append('%autoreload 2')
c.InteractiveShellApp.exec_lines.append('%config Application.verbose_crash=False')

def tweak():
  print("Enabling tweaks")

  try:
    import numpy as np
    np.set_printoptions(edgeitems=30, linewidth=100000)
  except Exception as e:
    print("Failed to tweak numpy. Is it installed?")

  try:
    import ssl;
    ssl._create_default_https_context = ssl._create_unverified_context
  except Exception as e:
    print("Failed to tweak ssl. Is it installed?")

  try:
    import matplotlib;
    matplotlib.use('Qt5Agg');
    import matplotlib.pyplot;
    matplotlib.pyplot.ioff()
  except Exception as e:
    print("Failed to tweak matplotlib. Is it installed?")

tweak()
EOF

ipython3 --profile-dir=$PROJECT_SOURCE/.ipython-profile -i "$@"

