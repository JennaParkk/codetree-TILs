# returns true if (x, y) is in range
def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


# returns true if the current cell contains trees (벽이 아님 +  빈칸이 아님)
def has_trees(x, y):
    return main_grid[x][y] > 0


# returns true if no trees, not a wall, not sprayed
def is_empty(x, y):
    return main_grid[x][y] == 0 and sprayed[x][y] == 0


# [1] 나무 성장: 네방향 탐색 후, 나무가 있는 칸의 수만큼 성장
def grow():

    for x in range(n):
        for y in range(n):
            # 나무가 있는 칸
            if has_trees(x, y):
                # 현재 좌표 : (x, y)
                cell_cnt = 0        # counts the number of cells that have trees

                # 4 방향 탐색
                for d in range(4):
                    nx = x + dx[d]
                    ny = y + dy[d]

                    # 나무가 있는 경우 + range check
                    if in_range(nx, ny):
                        if has_trees(nx, ny):  # 나무가 있는 경우
                            cell_cnt += 1

                # 현재 칸에 cell_cnt 만큼 나무 추가
                main_grid[x][y] += cell_cnt


# [2] 나무 번식: 나무가 있는 칸 마다 4 방향 탐색 후, 빈칸에 나무 더하기
def spread():
    # initialize a temporary grid to store the numbers of trees to add
    to_add = [[0] * n for _ in range(n)]

    # main grid 탐색 하면서 나무가 있는 칸 마다
    for x in range(n):
        for y in range(n):
            if has_trees(x, y):     # 나무가 있는 칸이면
                empty_cnt = 0      # initialize 빈칸의 갯수
                # 네 방향 탐색 후, 빈칸의 갯수 구하기
                for d in range(4):
                    nx = x + dx[d]
                    ny = y + dy[d]
                    # range check
                    if in_range(nx, ny):
                        # if in range, 빈칸인 경우, increment empty_cnt
                        if is_empty(nx, ny):
                            empty_cnt += 1

                # number of trees to add = current cell / number of empty cells
                if empty_cnt > 0:
                    add_cnt = main_grid[x][y] // empty_cnt

                    # temporary grid 에 추가할 나무의 갯수 저장
                    for d in range(4):
                        nx = x + dx[d]
                        ny = y + dy[d]
                        # range check
                        if in_range(nx, ny):
                            # if in range, 빈칸인 경우, add_cnt 만큼 temporary grid에 추가
                            if is_empty(nx, ny):
                                to_add[nx][ny] += add_cnt

    # main_grid 탐색 후, to_add 에 저장된 값 main 에 추가
    for x in range(n):
        for y in range(n):
            if to_add[x][y] > 0:
                main_grid[x][y] += to_add[x][y]


# [3] 제초제: 나무가 있는 각 칸에 제초제를 뿌렸을 때 박멸되는 나무의 수 저장 --> 최대값 위치 찾기 --> 그 위치에 제초제 뿌리기
def spray():

    max_kill = 0
    max_x, max_y = 0, 0
    # (1) 제초제 뿌렸을 때 박멸되는 나무의 수 저장
    # grid 돌면서 나무가 있는칸 찾기 (행 다음 열)
    for x in range(n):
        for y in range(n):
            if has_trees(x, y):     # 현재 칸에 나무가 있는 경우
                kill_cnt = main_grid[x][y]      # 현재 칸에 있는 나무의 수 +
                # 대각선으로 4방향 (k 만큼)

                for ddx, ddy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    for d in range(1, k + 1):
                        nx = x + d * ddx
                        ny = y + d * ddy

                        # range check
                        if in_range(nx, ny):
                            if has_trees(nx, ny):   # 그 칸에 나무가 있으면
                                kill_cnt += main_grid[nx][ny]       # kill_cnt 에 추가
                            else:   # 나무가 없으면 (벽, 빈칸, or 제초제)
                                break
                        else:
                            break

                # compare w/ current max
                if kill_cnt > max_kill:     # if greater
                    max_kill = kill_cnt     # update max
                    max_x = x
                    max_y = y

    # (2) 제초제 뿌리기
    # 대각선으로 4 방향 (k 만큼)
    main_grid[max_x][max_y] = 0     # 제초제 뿌리는 칸에 나무 박멸

    for ddx, ddy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        for d in range(k):
            nx = max_x + d * ddx
            ny = max_y + d * ddy

            if not in_range(nx, ny):
                break
            sprayed[nx][ny] = c
            if not has_trees(nx, ny):
                break
            main_grid[nx][ny] = 0
            
    return max_kill


# 1 년 지날 때 마다, 1씩 감소
def update_sprayed():
    for x in range(n):
        for y in range(n):
            if sprayed[x][y] > 0:
                sprayed[x][y] -= 1


dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]
#   첫 번째 줄에 격자의 크기 n, 박멸이 진행되는 년 수 m, 제초제의 확산 범위 k, 제초제가 남아있는 년 수 c가 공백을 사이에 두고 주어집니다
n, m, k, c = map(int, input().split())
main_grid = []      # n x n main grid
sprayed = [[0] * n for _ in range(n)]
ans = 0
for _ in range(n):
    main_grid.append(list(map(int, input().split())))

# m 년 동안 진행
for _ in range(m):

    # [1] 나무 성장
    grow()

    # [2] 나무 번식
    spread()

    # [3] 제초제
    ans += spray()

    # [4] update number of years remained (-1)
    update_sprayed()


print(ans)