#!/usr/bin/env python3
"""raft_consensus - Simplified Raft consensus simulation."""
import sys,random,time
class RaftNode:
    def __init__(s,nid,peers):s.id=nid;s.peers=peers;s.state="follower";s.term=0;s.voted_for=None;s.log=[];s.commit_idx=-1;s.leader=None
    def request_vote(s,candidate_term,candidate_id):
        if candidate_term>s.term:s.term=candidate_term;s.state="follower";s.voted_for=None
        if candidate_term>=s.term and s.voted_for in(None,candidate_id):s.voted_for=candidate_id;return True
        return False
    def start_election(s):
        s.term+=1;s.state="candidate";s.voted_for=s.id;votes=1
        for p in s.peers:
            if p.request_vote(s.term,s.id):votes+=1
        if votes>len(s.peers)//2:s.state="leader";s.leader=s.id
        else:s.state="follower"
    def append_entry(s,entry):
        if s.state!="leader":return False
        s.log.append({"term":s.term,"data":entry});s.commit_idx=len(s.log)-1;return True
def simulate(n=5,rounds=10):
    nodes=[RaftNode(i,[]) for i in range(n)]
    for nd in nodes:nd.peers=[p for p in nodes if p.id!=nd.id]
    leader_id=random.randint(0,n-1);nodes[leader_id].start_election()
    for nd in nodes:
        if nd.state=="leader":print(f"Node {nd.id} elected leader (term {nd.term})")
    for i in range(rounds):
        leader=[nd for nd in nodes if nd.state=="leader"]
        if leader:leader[0].append_entry(f"cmd_{i}");print(f"  Round {i}: committed cmd_{i}")
    return nodes
if __name__=="__main__":
    nodes=simulate();leader=[n for n in nodes if n.state=="leader"][0]
    print(f"\nLeader log: {len(leader.log)} entries")
