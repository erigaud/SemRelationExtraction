import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import ipdb
import numpy as np


class SkipGramModel(nn.Module):
    """Skip gram model of word2vec.

    Attributes:
        pair_emb_size : Number of pairs
        emb_size: Number of context words
        emb_dimention: Embedding dimention, typically from 50 to 500.
        
    """

    def __init__(self, emb_size, emb_dimension, pair_emb_dimension):
        """Initialize model parameters.

        Apply for two embedding layers.
        Initialize layer weight

        Args:
            emb_size: Embedding size.
            emb_dimention: Embedding dimention, typically from 50 to 500.

        Returns:
            None
        """
        super(SkipGramModel, self).__init__()
        self.emb_size = emb_size
        #self.pair_emb_size = pair_emb_size
        self.emb_dimension = emb_dimension
        self.pair_emb_dimension = pair_emb_dimension
        
        self.u_embeddings = nn.Embedding(self.emb_size, self.emb_dimension, sparse=True)  # |V| x d
        self.transitionMatrix = nn.Linear(2*self.emb_dimension, self.pair_emb_dimension)       # 2*d x d
        self.v_embeddings = nn.Embedding(self.emb_size, self.pair_emb_dimension, sparse=True)  # d   x |V|
        
        self.init_emb()
        
        
        print("Model parameters")
        #print("self.pair_emb_size :\t",self.pair_emb_size)
        print("self.emb_dimension :\t",self.emb_dimension)
        print("self.emb_size :\t",self.emb_size)
        print(self.u_embeddings)
        print(self.transitionMatrix)
        print(self.v_embeddings)
        
        
    def init_emb(self):
        """Initialize embedding weight like word2vec.

        The u_embedding is a uniform distribution in [-0.5/emb_size, 0.5/emb_size], and the elements of v_embedding are zeroes.

        Returns:
            None
        """
        initrange = 0.5 / self.emb_dimension
        self.u_embeddings.weight.data.uniform_(-initrange, initrange)
        self.v_embeddings.weight.data.uniform_(-0, 0)

    def forward(self, pos_u, pos_v, neg_v):
        """Forward process.

        As pytorch designed, all variables must be batch format, so all input of this method is a list of word id.

        Args:
            pos_u: list of center word ids for positive word pairs.
            pos_v: list of neighbor word ids for positive word pairs.
            neg_u: list of center word ids for negative word pairs.
            neg_v: list of neighbor word ids for negative word pairs.

        Returns:
            Loss of this process, a pytorch variable.
        """
        
        
       
        
        emb_w1 = self.u_embeddings(pos_u[:,0])
        emb_w2 = self.u_embeddings(pos_u[:,1])
        
        emb_pair = torch.cat([emb_w1,emb_w2],dim=1)             #Pair embedding representation (asymmetric relations)
        emb_rel = self.transitionMatrix(emb_pair)         #Relation embedding 
        
        emb_v = self.v_embeddings(pos_v)                 #context vector is for a pair of words.
        neg_emb_v = self.v_embeddings(neg_v)
        
        
        
        #print("Positive U embed :",emb_u.data.shape,"\n")
        #print("Positive V embed:",emb_v.data.shape,"\n")
        #print("Negative V embed:",neg_emb_v.data.shape,"\n")
        
        
        score = torch.mul(emb_rel, emb_v).squeeze()
        score = torch.sum(score, dim=1) # summed up for the dot product sum
        score = F.logsigmoid(score)
        
        
        neg_score = torch.bmm(neg_emb_v, emb_rel.unsqueeze(2)).squeeze() 
        neg_score = F.logsigmoid(-1 * neg_score)
        
        #print("\n emb_u", emb_u)
        #print("\n emb_v", emb_v)
        #print("\n score",score)
        #print("\n Neg_emb_v", neg_emb_v)
        #print("\n neg_score",neg_score)
        
        
        
        return -1 * (torch.sum(score)+torch.sum(neg_score)) #this has k values being summed up

    
    def save_embedding(self, id2word, file_name, use_cuda):
        """Save all embeddings to file.

        As this class only record pair id, so the map from id to pair has to be transfered from outside.

        Args:
            id2pair: map from pair id to pair.
            file_name: file name.
        Returns:
            None.
        """
        if use_cuda:
            embedding = self.u_embeddings.weight.cpu().data.numpy()
        else:
            embedding = self.u_embeddings.weight.data.numpy()
            
        fout = open(file_name, 'w')
        fout.write('%d %d\n' % (len(id2word), self.emb_dimension))
        for wid, w in id2word.items():
            e = embedding[wid]
            e = ' '.join(map(lambda x: str(x), e))
            fout.write('%s %s\n' % (w, e))

        '''
         Save transitionMatrix
         
        '''
        #fout = open(file_name+"_TransitionMatrix", 'w')
        
        if use_cuda:
            tWeightMatrix = self.transitionMatrix.weight.cpu().data.numpy()
            tBiasMatrix = self.transitionMatrix.bias.cpu().data.numpy()
        else:
            tWeightMatrix = self.transitionMatrix.weight.data.numpy()
            tBiasMatrix = self.transitionMatrix.bias.data.numpy()
        
        np.savetxt(file_name+"_Weights",tWeightMatrix, fmt='%1.5f')
        np.savetxt(file_name+"_Bias",tBiasMatrix, fmt='%1.5f')
        
        
        #for index,items in enumerate(tWeightMatrix):
        #    fout.write("\n"+str(items)+str(tBiasMatrix[index]))

def test():
    model = SkipGramModel(100, 100)
    id2pair = dict()
    for i in range(100):
        id2pair[i] = str(i)
    model.save_embedding(id2pair)


if __name__ == '__main__':
    test()