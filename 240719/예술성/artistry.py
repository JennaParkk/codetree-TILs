import sys

# returns true if in range
def in_range(x, y):
    return 0 <= x < n and 0 <= y < n


# rotate n x n square clockwise
def rotate(sx, sy, sq_n):
    for x in range(sx, sx + sq_n):
            # ox, oy 바꿔주기
        for y in range(sy, sy + sq_n):
            ox = x - sx
            oy = y - sy
            rx = oy
            ry = sq_n - ox - 1
            # update grid_rotated
            grid_rotated[rx + sx][ry + sy] = main_grid[x][y]


# 십자가 회전 후, grid_rotated 에 저장
def rotate_cross():
   for x in range(n):
       for y in range(n):
           if y == n // 2:
               grid_rotated[y][x] = main_grid[x][y]
           elif x == n // 2:
               grid_rotated[n - y - 1][x] = main_grid[x][y]



# [2] 미술점수 계산
def calculate_between():
    score = 0
    # (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수 ) x 그룹 a를 이루고 있는 숫자 값 x 그룹 b를 이루고 있는 숫자 값 x 그룹 a와 그룹 b가 서로 맞닿아 있는 변의 수
    for x in range(n):
        for y in range(n):
            for dx, dy in ([-1, 0], [0, -1], [0, 1], [1, 0]):
                nx = x + dx
                ny = y + dy
                if in_range(nx, ny):
                    if main_grid[nx][ny] != main_grid[x][y]:    # 다른 그룹이 맞닿아 있는 경우
                        # 두개의 그룹
                        g_a = main_grid[x][y]
                        g_b = main_grid[nx][ny]     # 그룹 a, b 를 이루고 있는 숫자 값
                        # get group number for each group
                        a_num = grid_divided[x][y]
                        b_num = grid_divided[nx][ny]
                        # group number 를 통해 group count 확인
                        a_cnt = group_cnt[a_num]
                        b_cnt = group_cnt[b_num]
                        # 그룹 a 를 이루고 있는 수 * 그룹 b 를 이루고 있는 수 * (a count + b count)
                        score += (a_cnt + b_cnt) * g_a * g_b

    # 각 combination 마다 2번씩 계산 되므로
    score = score // 2  # 2로 나눠주기

    return score


def dfs(sx, sy, gn):
    # (sx, sy) 부터 dfs 시작
    # gn : 현재 그룹의 그룹넘버
    current = main_grid[sx][sy]     # 현재 칸에 저장되었는 숫자

    # update visited
    visited[sx][sy] = 1

    # 4 방향 탐색
    for dx, dy in ([-1, 0], [1, 0], [0, 1], [0, -1]):
        nx = sx + dx
        ny = sy + dy
        # range check
        if in_range(nx, ny):
            if visited[nx][ny] == 0 and main_grid[nx][ny] == current:   # not visited + 같은 숫자가 저장되어 있는 칸일 경우
                group_cnt[gn] += 1  # 현재 그룹의 칸 수 증가
                grid_divided[nx][ny] = gn   # 그룹넘버로 나눠진 grid
                dfs(nx, ny, gn)


# [1] 그룹 나누기
def divide_groups():
    group_n = 0
    # (0,0) 부터 (n-1, n-1) 까지 모든 칸 탐색하며 그룹 시작점 찾기

    for x in range(n):
        for y in range(n):
            current = main_grid[x][y]   # 현재 칸에 저장된 숫자
            if visited[x][y] == 0:  # dfs 실행 전
                group_n += 1    # 1 부터 시작
                grid_divided[x][y] = group_n
                group_cnt.append(1) # 새로운 그룹에 갯수 1부터 시작
                dfs(x, y, group_n)   # 새로운 그룹 시작 지점부터 dfs 실행


n = int(input())
main_grid = []
score_total = 0

for _ in range(n):
    main_grid.append(list(map(int, input().split())))

for _ in range(4):
    grid_divided = [[0] * n for _ in range(n)]
    visited = [[0] * n for _ in range(n)]
    group_cnt = [0]

    # [1] 그룹 나누기
    divide_groups()
    # [2] 조화 점수 계산
    score_total += calculate_between()
    # [3] 회전 : 십자가 회전 + 4개의 정사각형 회전
    grid_rotated = [[0] * n for _ in range(n)]      # 초기화
    # 십자가 회전 후 새로운 grid 에 저장
    rotate_cross()
    # 나머지 4개의 정사각형 회전 후 grid 에 저장
    m = n // 2
    # 시작점 4개 (0,0) (m + 1, 0), (0, m + 1), (m + 1, m + 1)
    rotate(0, 0, m)
    rotate(m + 1, 0, m)
    rotate(0, m + 1, m)
    rotate(m + 1, m + 1, m)
    # update main_grid
    main_grid = grid_rotated

print(score_total)




'''
# anticlockwise rotation
def rotate_anticlock(sx, sy, sq_n):
    arr_next = [[0] * 10 for _ in range(10)]

    for x in range(sx, sx + sq_n):
        for y in range(sy, sy + sq_n):
            # (0, 0) 변경
            ox = sx - sq_n
            oy = sy - sq_n
            # x y coordinates after rotation
            rx = sq_n - oy - 1
            ry = ox
            arr_next[rx + sx][ry + sy] = main_grid[x][y]
'''

# clockwise rotation
'''
def rotate_clockwise(sx, sy, sq_n):
    next_arr = [[0] * 10 for _ in range(10)]

    for x in range(sx, sx + sq_n):
        for y in range(sy, sy + sq_n):
            # (0,0) 으로 변경
            ox = x - sx
            oy = y - sy
            rx = oy
            ry = sq_n - ox - 1
            next_arr[rx + sx][ry + sy] = main_grid[x][y]
'''