echo "Cloning Repo...."
if [ -z $BRANCH ]
then
  echo "Cloning main branch...."
  git clone https://github.com/nabilanavab/iLovePDF /iLovePDF
else
  echo "Cloning $BRANCH branch...."
  git clone https://github.com/nabilanavab/iLovePDF -b $BRANCH /iLovePDF
fi
cd /iLovePDF
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 pdf.py
