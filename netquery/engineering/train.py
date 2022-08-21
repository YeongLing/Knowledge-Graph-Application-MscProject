from argparse import ArgumentParser

from netquery.utils import *
from netquery.bio.data_utils import load_graph
from netquery.data_utils import load_queries_by_formula, load_test_queries_by_formula
from netquery.model import QueryEncoderDecoder
from netquery.train_helpers import run_train

from torch import optim

#Create a parser.（解析器)
parser = ArgumentParser()
#Making calls to the add_argument() method to fill the information into parser.
parser.add_argument("--embed_dim", type=int, default=128)
parser.add_argument("--data_dir", type=str, default="../../engineering_data")
parser.add_argument("--lr", type=float, default=0.01)
parser.add_argument("--depth", type=int, default=0)
parser.add_argument("--batch_size", type=int, default=512)
parser.add_argument("--max_iter", type=int, default=20000)
parser.add_argument("--max_burn_in", type=int, default=100000)
parser.add_argument("--val_every", type=int, default=5000)
parser.add_argument("--tol", type=float, default=0.0001)
parser.add_argument("--cuda", action='store_true')
parser.add_argument("--log_dir", type=str, default="./")
parser.add_argument("--model_dir", type=str, default="./")
parser.add_argument("--decoder", type=str, default="transe")
parser.add_argument("--inter_decoder", type=str, default="mean")
parser.add_argument("--opt", type=str, default="adam")
#ArgumentParser parses arguments through the parse_args() method.
#This will inspect the command line, convert each argument to the appropriate type and then invoke the appropriate action.
args = parser.parse_args()

print("Loading graph data..")
graph, feature_modules, node_maps = load_graph(args.data_dir, args.embed_dim)
if args.cuda:
    graph.features = cudify(feature_modules, node_maps)
out_dims = {mode:args.embed_dim for mode in graph.relations}

print("Loading edge data..")
#返回包含edge信息的三个字典 train_queries, val_queries, 和 test_queries
#train_queries={{ '1-chain' : {Fomula : [Query ,...] ,... } ,... }}
#val_queries={'full_neg' : {'1-chain' : {Formula : [Query ,...]}} , 'one_neg' : {'1-chain' : {Formula : [Query ,...]}}}
#test_queries={'full_neg' : {'1-chain' : {Formula : [Query ,...]}} , 'one_neg' : {'1-chain' : {Formula : [Query ,...]}}}
train_queries = load_queries_by_formula(args.data_dir + "/train_edges.pkl")
val_queries = load_test_queries_by_formula(args.data_dir + "/val_edges.pkl")
test_queries = load_test_queries_by_formula(args.data_dir + "/test_edges.pkl")

#用和提取edge信息同样的方法，将querydata也提取出来（均使用load_queries_by_formula()函数)
#The "update()" method updates the dictionary with the elements from another dictionary object or from an iterable of key/value pairs.
#Note: the "update()" method adds element(s) to the dictionary if the key is not in the dictionary. If the key is in the dictionary, it updates the key with new value.
print("Loading query data..")
for i in range(2,4):
    train_queries.update(load_queries_by_formula(args.data_dir + "/train_queries_{:d}.pkl".format(i)))
    i_val_queries = load_test_queries_by_formula(args.data_dir + "/val_queries_{:d}.pkl".format(i))
    val_queries["one_neg"].update(i_val_queries["one_neg"])
    val_queries["full_neg"].update(i_val_queries["full_neg"])
    i_test_queries = load_test_queries_by_formula(args.data_dir + "/test_queries_{:d}.pkl".format(i))
    test_queries["one_neg"].update(i_test_queries["one_neg"])
    test_queries["full_neg"].update(i_test_queries["full_neg"])


enc = get_encoder(args.depth, graph, out_dims, feature_modules, args.cuda)
dec = get_metapath_decoder(graph, enc.out_dims if args.depth > 0 else out_dims, args.decoder)
inter_dec = get_intersection_decoder(graph, out_dims, args.inter_decoder)
    
enc_dec = QueryEncoderDecoder(graph, enc, dec, inter_dec)
if args.cuda:
    enc_dec.cuda()

if args.opt == "sgd":
    optimizer = optim.SGD(filter(lambda p : p.requires_grad, enc_dec.parameters()), lr=args.lr, momentum=0)
elif args.opt == "adam":
    optimizer = optim.Adam(filter(lambda p : p.requires_grad, enc_dec.parameters()), lr=args.lr)
    
log_file = args.log_dir + "/{data:s}-{depth:d}-{embed_dim:d}-{lr:f}-{decoder:s}-{inter_decoder:s}.log".format(
        data=args.data_dir.strip().split("/")[-1],
        depth=args.depth,
        embed_dim=args.embed_dim,
        lr=args.lr,
        decoder=args.decoder,
        inter_decoder=args.inter_decoder)
model_file = args.model_dir + "/{data:s}-{depth:d}-{embed_dim:d}-{lr:f}-{decoder:s}-{inter_decoder:s}.log".format(
        data=args.data_dir.strip().split("/")[-1],
        depth=args.depth,
        embed_dim=args.embed_dim,
        lr=args.lr,
        decoder=args.decoder,
        inter_decoder=args.inter_decoder)
logger = setup_logging(log_file)

run_train(enc_dec, optimizer, train_queries, val_queries, test_queries, logger,max_iter=args.max_iter, max_burn_in=args.max_burn_in, val_every=args.val_every, model_file=model_file)
torch.save(enc_dec.state_dict(), model_file)
