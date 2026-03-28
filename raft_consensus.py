#!/usr/bin/env python3
"""Simplified Raft consensus simulation."""
import sys,random,time
class Node:
    def __init__(self,id,peers):
        self.id=id;self.peers=peers;self.state='follower'
        self.term=0;self.voted_for=None;self.log=[];self.commit_idx=-1
        self.votes=0
    def request_vote(self,candidate_term,candidate_id):
        if candidate_term>self.term:
            self.term=candidate_term;self.voted_for=None;self.state='follower'
        if candidate_term>=self.term and self.voted_for in (None,candidate_id):
            self.voted_for=candidate_id;return True
        return False
    def start_election(self,nodes):
        self.term+=1;self.state='candidate';self.voted_for=self.id;self.votes=1
        for p in self.peers:
            if nodes[p].request_vote(self.term,self.id): self.votes+=1
        if self.votes>len(self.peers)//2+1:
            self.state='leader';return True
        return False
    def append_entry(self,entry):
        if self.state!='leader': return False
        self.log.append((self.term,entry));return True
    def __repr__(self): return f"Node({self.id}, {self.state}, term={self.term}, log={len(self.log)})"
def main():
    random.seed(42)
    ids=list(range(5))
    nodes={i:Node(i,[j for j in ids if j!=i]) for i in ids}
    # Node 2 starts election
    won=nodes[2].start_election(nodes)
    print(f"Node 2 election: {'won' if won else 'lost'}")
    for n in nodes.values(): print(f"  {n}")
    # Leader appends entries
    leader=nodes[2]
    for entry in ["SET x=1","SET y=2","DEL z"]:
        leader.append_entry(entry)
    print(f"\nLeader log: {leader.log}")
if __name__=="__main__": main()
