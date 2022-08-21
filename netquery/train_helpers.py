import numpy as np
from netquery.utils import eval_auc_queries, eval_perc_queries
import torch

def check_conv(vals, window=2, tol=1e-4):
    if len(vals) < 2 * window:
        return False
    #conv表示vals末尾窗口内元素的平均值减倒数第二个窗口内元素的平均值
    conv = np.mean(vals[-window:]) - np.mean(vals[-2*window:-window])
    #检查conv是否小于tol，小于返回True，大于返回False
    return conv < tol
#定义：用指数移动平均(Exponential Moving Average, EMA)法来计算平均值ema_loss
def update_loss(loss, losses, ema_loss, ema_alpha=0.01):
    losses.append(loss)
    if ema_loss is None:
        ema_loss = loss
    else:
        ema_loss = (1-ema_alpha)*ema_loss + ema_alpha*loss
    return losses, ema_loss

def run_eval(model, queries, iteration, logger, by_type=False):
    vals = {}
    def _print_by_rel(rel_aucs, logger):
        for rels, auc in rel_aucs.iteritems():
            logger.info(str(rels) + "\t" + str(auc))
    for query_type in queries["one_neg"]:
        auc, rel_aucs = eval_auc_queries(queries["one_neg"][query_type], model)
        perc = eval_perc_queries(queries["full_neg"][query_type], model)
        vals[query_type] = auc
        logger.info("{:s} val AUC: {:f} val perc {:f}; iteration: {:d}".format(query_type, auc, perc, iteration))
        if by_type:
            _print_by_rel(rel_aucs, logger)
        if "inter" in query_type:
            auc, rel_aucs = eval_auc_queries(queries["one_neg"][query_type], model, hard_negatives=True)
            perc = eval_perc_queries(queries["full_neg"][query_type], model, hard_negatives=True)
            logger.info("Hard-{:s} val AUC: {:f} val perc {:f}; iteration: {:d}".format(query_type, auc, perc, iteration))
            if by_type:
                _print_by_rel(rel_aucs, logger)
            vals[query_type + "hard"] = auc
    return vals

def run_train(model, optimizer, train_queries, val_queries, test_queries, logger,
        max_burn_in =100000, batch_size=512, log_every=100, val_every=1000, tol=1e-6,
        max_iter=int(2*10e4), inter_weight=0.005, path_weight=0.01, model_file=None):
    edge_conv = False
    ema_loss = None #指数移动平均(EMA)，是一种给予近期数据更高权重的平均方法
    vals = []
    losses = [] #存储loss数据的数组
    conv_test = None
    for i in range(max_iter):
        
        optimizer.zero_grad()
        loss = run_batch(train_queries["1-chain"], model, i, batch_size)
        #检查model是否收敛
        if not edge_conv and (check_conv(vals) or len(losses) >= max_burn_in):
            logger.info("Edge converged at iteration {:d}".format(i-1))
            logger.info("Testing at edge conv...")
            conv_test = run_eval(model, test_queries, i, logger)
            conv_test = np.mean(conv_test.values())
            edge_conv = True
            losses = []
            ema_loss = None
            vals = []
            if not model_file is None:
                torch.save(model.state_dict(), model_file+"-edge_conv")
        
        if edge_conv:
            for query_type in train_queries:
                if query_type == "1-chain":
                    continue
                if "inter" in query_type:
                    loss += inter_weight*run_batch(train_queries[query_type], model, i, batch_size)
                    loss += inter_weight*run_batch(train_queries[query_type], model, i, batch_size, hard_negatives=True)
                else:
                    loss += path_weight*run_batch(train_queries[query_type], model, i, batch_size)
            if check_conv(vals):
                    logger.info("Fully converged at iteration {:d}".format(i))
                    break
        #原为losses, ema_loss = update_loss(loss.data[0], losses, ema_loss)
        losses, ema_loss = update_loss(loss.item(), losses, ema_loss)
        loss.backward()
        optimizer.step()
            
        if i % log_every == 0:
            logger.info("Iter: {:d}; ema_loss: {:f}".format(i, ema_loss))
            
        if i >= val_every and i % val_every == 0:
            v = run_eval(model, val_queries, i, logger)
            if edge_conv:
                vals.append(np.mean(v.values()))
            else:
                vals.append(v["1-chain"])
    
    v = run_eval(model, test_queries, i, logger)
    logger.info("Test macro-averaged val: {:f}".format(np.mean(list(v.values()))))
    logger.info("Improvement from edge conv: {:f}".format((np.mean(list(v.values()))-conv_test)/conv_test))

def run_batch(train_queries, enc_dec, iter_count, batch_size, hard_negatives=False):
    num_queries = [float(len(queries)) for queries in train_queries.values()]
    denom = float(sum(num_queries))
    #np.argmax(a，axis=None)，输入数组a，返回数组a沿axis轴方向（默认为水平方向）最大值的索引
    #np.random.multinomial(n,pvals,size=None)进行n次实验，返回每种可能出现的次数
        #n:实验次数
        # pvals:长度为p的浮点数序列，pvals包含每个不同结果的概率，这些总和必须为1。（但是，pvals[-1]始终用来表示剩余概率）
    formula_index = np.argmax(np.random.multinomial(1, 
            np.array(num_queries)/denom))
    #原为formula = train_queries.keys()[formula_index]
    formula = list(train_queries.keys())[formula_index]
    n = len(train_queries[formula])
    start = (iter_count * batch_size) % n
    end = min(((iter_count+1) * batch_size) % n, n)
    end = n if end <= start else end
    queries = train_queries[formula][start:end]
    loss = enc_dec.margin_loss(formula, queries, hard_negatives=hard_negatives)
    return loss
