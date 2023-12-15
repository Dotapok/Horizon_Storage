
export CLUSTER_SECRET=$(od -vN 32 -An -tx1 /dev/urandom | tr -d ' \n')
# echo $CLUSTER_SECRET
docker-compose up -d cluster0 ipfs0 ipfs1 ipfs2 ipfs3 ipfs4