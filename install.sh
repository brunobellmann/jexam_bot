cp jexam-node.service /lib/systemd/system/
cp jexam-python.service /lib/systemd/system/
systemctl enable --now jexam-node
systemctl enable --now jexam-python