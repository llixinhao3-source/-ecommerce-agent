"""
定时任务调度器
Task Scheduler

支持：
- 定时任务
- 循环任务
- 一次性任务
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Callable, Optional, List
from croniter import croniter
import json
from pathlib import Path


class Task:
    """任务定义"""
    
    def __init__(self, task_id: str, name: str, schedule: str, callback: Callable, 
                 enabled: bool = True, **kwargs):
        self.task_id = task_id
        self.name = name
        self.schedule = schedule  # cron表达式或 interval (秒)
        self.callback = callback
        self.enabled = enabled
        self.kwargs = kwargs
        self.last_run: Optional[datetime] = None
        self.next_run: Optional[datetime] = None
        self.run_count = 0
        
        # 计算下次执行时间
        self.update_next_run()
    
    def update_next_run(self):
        """更新下次执行时间"""
        if self.schedule.isdigit():
            # 间隔任务
            interval = int(self.schedule)
            if self.last_run:
                self.next_run = self.last_run + timedelta(seconds=interval)
            else:
                self.next_run = datetime.now()
        else:
            # Cron任务
            try:
                cron = croniter(self.schedule, datetime.now())
                self.next_run = cron.get_next(datetime)
            except:
                self.next_run = None
    
    def should_run(self) -> bool:
        """检查是否应该执行"""
        if not self.enabled:
            return False
        if self.next_run is None:
            return False
        return datetime.now() >= self.next_run
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "schedule": self.schedule,
            "enabled": self.enabled,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "run_count": self.run_count
        }


class Scheduler:
    """任务调度器"""
    
    def __init__(self, state_file: str = "./memory/scheduler_state.json"):
        self.tasks: Dict[str, Task] = {}
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
        # 加载状态
        self.load_state()
    
    def add_task(self, task_id: str, name: str, schedule: str, callback: Callable,
                 enabled: bool = True, **kwargs) -> Task:
        """添加任务"""
        task = Task(task_id, name, schedule, callback, enabled, **kwargs)
        self.tasks[task_id] = task
        self.save_state()
        return task
    
    def remove_task(self, task_id: str):
        """移除任务"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_state()
    
    def enable_task(self, task_id: str, enabled: bool = True):
        """启用/禁用任务"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = enabled
            self.save_state()
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """列出所有任务"""
        return [task.to_dict() for task in self.tasks.values()]
    
    def run_task(self, task_id: str) -> bool:
        """手动执行任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        try:
            result = task.callback(**task.kwargs)
            task.last_run = datetime.now()
            task.run_count += 1
            task.update_next_run()
            self.save_state()
            return True
        except Exception as e:
            print(f"任务执行失败: {task.name} - {e}")
            return False
    
    def _run_loop(self):
        """运行循环"""
        while self.running:
            now = datetime.now()
            
            for task in self.tasks.values():
                if task.should_run():
                    print(f"执行任务: {task.name}")
                    try:
                        task.callback(**task.kwargs)
                        task.last_run = now
                        task.run_count += 1
                        task.update_next_run()
                    except Exception as e:
                        print(f"任务执行失败: {task.name} - {e}")
            
            self.save_state()
            time.sleep(1)  # 每秒检查一次
    
    def start(self):
        """启动调度器"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("调度器已启动")
    
    def stop(self):
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("调度器已停止")
    
    def save_state(self):
        """保存状态"""
        try:
            state = {
                "tasks": [task.to_dict() for task in self.tasks.values()]
            }
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存状态失败: {e}")
    
    def load_state(self):
        """加载状态"""
        if not self.state_file.exists():
            return
        
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # 恢复任务状态（但不恢复callback）
            for task_data in state.get("tasks", []):
                # 注意：callback无法恢复，需要重新注册
                pass
        except Exception as e:
            print(f"加载状态失败: {e}")


# 示例用法
def example_task(**kwargs):
    """示例任务"""
    print(f"任务执行: {datetime.now()}")


if __name__ == "__main__":
    # 创建调度器
    scheduler = Scheduler()
    
    # 添加定时任务
    # 每5秒执行一次
    scheduler.add_task(
        task_id="example_1",
        name="示例任务1",
        schedule="5",  # 5秒
        callback=example_task
    )
    
    # 每天9点执行 (使用cron表达式)
    # scheduler.add_task(
    #     task_id="daily_task",
    #     name="每日任务",
    #     schedule="0 9 * * *",  # 每天9点
    #     callback=example_task
    # )
    
    # 启动
    scheduler.start()
    
    # 运行60秒后停止
    time.sleep(60)
    scheduler.stop()
