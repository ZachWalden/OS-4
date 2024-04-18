# ZACH WALDEN
# w989j327
# OS Programming Project 4: Page Replacement 

#Import queue to be used in each algo
from collections import deque

# FIFO Algorithm. First page in, first page to be removed when full. 
def FIFO_algo(pages, max_capacity):
    #initialize the queue & and the set of existing pages
    page_queue = deque()
    page_set = set()
    page_faults = 0

    print("FIFO Algorithm:")
    #loop through pages
    for i, page in enumerate(pages, start=1):
        #fill page table if not full
        if len(page_set) < max_capacity:
            if page not in page_set:
                page_set.add(page)
                page_faults += 1
                page_queue.append(page)

                # Output resulting fault
                print(f"Step {i}: Page fault ({page}) - Page Table: {page_set}, Frames: {list(page_queue)}, Faults: {page_faults}")

        else: #pop furthest item, add new page in
            if page not in page_set:
                val = page_queue.popleft()
                page_set.remove(val)
                page_set.add(page)
                page_queue.append(page)
                page_faults += 1
                
                # Output resulting fault
                print(f"Step {i}: Page fault ({page}) - Page Table: {page_set}, Frames: {list(page_queue)}, Faults: {page_faults}")

    #Print total faults after going through all pages
    print(f"Total Page Faults: {page_faults}")

# Least recently used algorithm. Least used elemnt is the first element to be removed to make room for new page
def LRU_algo(reference_string, max_capacity):
    # Initialize queue, total hits & faults
    pages = deque(maxlen=max_capacity)
    faults = 0
    hits = 0

    print("LRU Algorithm:")
    for i, ref_page in enumerate(reference_string, start=1):
        # If the current page is in the queue, move it to the front so it won't be removed
        # hence "least recently used"
        if ref_page in pages:
            pages.remove(ref_page)
            pages.append(ref_page)
            hits += 1
        else: # If the page is not in the queue:
            faults += 1 # Add Fault

            #W Add to list if not full
            if len(pages) < max_capacity:
                pages.append(ref_page)
            else: # If full, remove least recently used.
                pages.popleft()
                pages.append(ref_page)
            
            # Print page fault result
            print(f"Step {i}: Page fault ({ref_page}) - Page Table: {set(pages)}, Frames: {list(pages)}, Faults: {faults}")

    # Output algo's total page faults
    print(f"Total Page Faults: {faults}")

# Optimal Algorithm
def optimal_algo(reference_string, max_capacity):
    #Start with empty list of frames, initalize 0 faults & hits
    frames = []
    faults = 0
    hits = 0

    print("Optimal Algorithm:")
    # Function for predicting the upcoming page
    def predict_page(page, frames, page_number, page_index):
        farthest_page = page_index
        result = -1
        for i in range(len(frames)):
            for j in range(page_index, page_number):
                if frames[i] == page[j]:
                    if j > farthest_page:
                        farthest_page = j
                        result = i
                    break
            if j == page_number - 1:
                return i

        if result == -1:
            return 0
        else:
            return result

    # Function for quickly verifying if the element is in the current frame list
    def search_page(key, frames):
        return key in frames

    # Optimal Algorithm: utilize previous functions for page table 
    for i, ref_page in enumerate(reference_string, start=1):
        if search_page(ref_page, frames):
            hits += 1
            continue

        if len(frames) < max_capacity:
            frames.append(ref_page)
        else:
            j = predict_page(reference_string, frames, len(reference_string), i)
            frames[j] = ref_page
        faults += 1
        print(f"Step {i}: Page fault ({ref_page}) - Page Table: {set(frames)}, Frames: {list(frames)}, Faults: {faults}")

    print(f"Total Page Faults: {faults}")

# Sample Input given in assignment:
reference_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
max_capacity = 4

# Feed given input into each of our algorithms. Each is printed within their respective functions.
FIFO_algo(reference_string, max_capacity)
print("\n")
LRU_algo(reference_string, max_capacity)
print("\n")
optimal_algo(reference_string, max_capacity)

