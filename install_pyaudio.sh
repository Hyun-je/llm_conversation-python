sudo apt-get remove libportaudio2
sudo apt-get install libasound2-dev

git clone -b alsapatch https://github.com/gglockner/portaudio
cd portaudio
./configure && make
sudo make install
sudo ldconfig
cd ..
rm -rf portaudio

sudo pip install pyaudio --break-system-packages