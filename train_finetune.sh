CONFIG=$1
GPUS=$2
# MODEL_NAME=$(basename "$(dirname $CONFIG)")
MODEL_NAME=KR-test

PORT=10902

while : # auto-resume: the code sometimes crash due to bug of gloo on some gpus
do
torchrun --nproc_per_node=$GPUS \
        --master_port=$PORT \
    melo/train.py --c $CONFIG --model $MODEL_NAME --pretrain_G logs/$MODEL_NAME/G_0.pth --pretrain_D logs/$MODEL_NAME/D.pth --pretrain_dur logs/$MODEL_NAME/DUR.pth 

for PID in $(ps -aux | grep $CONFIG | grep python | awk '{print $2}')
do
    echo $PID
    kill -9 $PID
done
sleep 30
done
