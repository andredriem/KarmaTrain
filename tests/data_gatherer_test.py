import karmatrain.data_gatherer

if __name__ == '__main__':
    #TODO make proper test
    gather = karmatrain.data_gatherer.SubredditGather('the_donald', 500, 24, 30)
    gather.watch()
    pass
